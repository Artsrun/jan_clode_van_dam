"""Telegram /forums command – search & analyse tech forum discussions via Claude AI."""

import logging
from urllib.parse import quote_plus

from telegram import Update
from telegram.ext import ContextTypes

from utils.claude_client import ask_claude
from utils.fetcher import fetch_feed, fetch_page_text

logger = logging.getLogger(__name__)

# Public tech forum RSS feeds that support search or browsing by tag/keyword
FORUM_SOURCES = [
    {
        "name": "Stack Overflow",
        "rss": "https://stackoverflow.com/feeds/tag/{query}",
        "tag_sep": "+",
    },
    {
        "name": "Hacker News",
        "rss": "https://hnrss.org/newest?q={query}&count=5",
        "tag_sep": "+",
    },
    {
        "name": "Reddit r/programming",
        "rss": "https://www.reddit.com/r/programming/search.json?q={query}&sort=new&limit=5",
        "tag_sep": "+",
    },
    {
        "name": "Dev.to",
        "rss": "https://dev.to/search/feed_content?per_page=5&page=0&search_fields={query}",
        "tag_sep": "%20",
    },
]

SYSTEM_PROMPT = """You are a senior software engineer and tech forum analyst.
You have been given excerpts from multiple tech forum discussions on a specific topic.
Your job is to:
1. Summarise the key discussion points and expert opinions.
2. Highlight any consensus, controversies, or notable insights.
3. List the most useful links shared.
4. Give a brief "TL;DR" at the top.

Format your response as plain text with clear sections.
Keep the response under 800 words."""


def _build_rss_url(template: str, query: str, sep: str) -> str:
    """Build a forum RSS URL from a template, substituting the query."""
    encoded = quote_plus(query).replace("+", sep)
    return template.format(query=encoded)


async def forums_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /forums <topic> command."""
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a topic to search.\n"
            "Usage: `/forums Python asyncio best practices`",
            parse_mode="Markdown",
        )
        return

    topic = " ".join(context.args).strip()
    await update.message.reply_text(
        f"🔎 Searching tech forums for *{topic}* …",
        parse_mode="Markdown",
    )

    collected_text = ""

    # Try Stack Overflow and Hacker News RSS feeds (most reliable)
    for source in FORUM_SOURCES[:2]:
        url = _build_rss_url(source["rss"], topic, source["tag_sep"])
        entries = fetch_feed(url, max_entries=5)
        if entries:
            collected_text += f"\n\n=== {source['name']} ===\n"
            for entry in entries:
                collected_text += (
                    f"• {entry['title']}\n"
                    f"  Link: {entry['link']}\n"
                    f"  {entry['summary'][:400]}\n"
                )

    # If RSS gave us very little, try Hacker News Algolia search page
    if len(collected_text) < 300:
        hn_url = f"https://hn.algolia.com/?q={quote_plus(topic)}&dateRange=pastYear&type=story"
        page_text = fetch_page_text(hn_url, max_chars=3000)
        if page_text:
            collected_text += f"\n\n=== Hacker News (web) ===\n{page_text}\n"

    if not collected_text.strip():
        await update.message.reply_text(
            "❌ Could not find forum discussions on that topic. "
            "Try rephrasing your query or check your internet connection."
        )
        return

    user_message = f"Tech forum discussions about: {topic}\n{collected_text}"

    try:
        analysis = ask_claude(SYSTEM_PROMPT, user_message)
        reply = f"🗣️ *Tech Forum Analysis: {topic}*\n\n{analysis}"
        await update.message.reply_text(
            reply, parse_mode="Markdown", disable_web_page_preview=True
        )
    except Exception as exc:
        logger.error("Forums handler error: %s", exc)
        await update.message.reply_text(
            "❌ An error occurred while analysing forums. Please try again later."
        )
