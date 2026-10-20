"""Telegram /feed command – fetch & summarise RSS/Atom tech feeds via Claude AI."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from utils.claude_client import ask_claude
from utils.fetcher import fetch_feed, is_valid_url

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a tech journalist and content curator.
You will receive a list of RSS feed entries (title, link, summary, published date).
Write a concise, engaging digest in plain text (no markdown headers, use bullet
points •). For each entry include: headline, one-sentence summary, and the link.
Keep the entire digest under 600 words. Sort by relevance / interest."""


async def feed_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /feed <url> command."""
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a feed URL.\n"
            "Usage: `/feed https://feeds.feedburner.com/TechCrunch`",
            parse_mode="Markdown",
        )
        return

    url = context.args[0].strip()
    if not is_valid_url(url):
        await update.message.reply_text(
            "❌ Invalid URL. Please provide a full URL starting with `http://` or `https://`.",
            parse_mode="Markdown",
        )
        return

    await update.message.reply_text(
        f"📡 Fetching feed `{url}` …", parse_mode="Markdown"
    )

    entries = fetch_feed(url, max_entries=8)
    if not entries:
        await update.message.reply_text(
            "❌ Could not fetch feed entries. Please check the URL and make sure it "
            "points to a valid RSS/Atom feed."
        )
        return

    # Build a structured text for Claude
    entries_text = ""
    for i, entry in enumerate(entries, 1):
        entries_text += (
            f"\n[{i}] Title: {entry['title']}\n"
            f"    Link: {entry['link']}\n"
            f"    Published: {entry['published']}\n"
            f"    Summary: {entry['summary'][:500]}\n"
        )

    user_message = f"Feed URL: {url}\n\nEntries:{entries_text}"

    try:
        digest = ask_claude(SYSTEM_PROMPT, user_message)
        reply = f"📰 *Tech Feed Digest*\n\n{digest}"
        await update.message.reply_text(
            reply, parse_mode="Markdown", disable_web_page_preview=True
        )
    except Exception as exc:
        logger.error("Feed handler error: %s", exc)
        await update.message.reply_text(
            "❌ An error occurred while summarising the feed. Please try again later."
        )
