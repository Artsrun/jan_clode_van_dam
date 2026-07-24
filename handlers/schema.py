"""Telegram /schema command – generate SEO JSON-LD schema markup via Claude AI."""

import json
import logging

from telegram import Update
from telegram.ext import ContextTypes

from utils.claude_client import ask_claude
from utils.fetcher import fetch_page_text, get_page_metadata, is_valid_url

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an SEO expert and JSON-LD schema specialist.
Given a web page's metadata and text content, produce a single valid JSON-LD
<script type="application/ld+json"> block that best represents the page.
Choose the most appropriate Schema.org type (e.g. Article, TechArticle,
WebPage, FAQPage, HowTo, Product, etc.).
Return ONLY the raw JSON object (no markdown fences, no explanation).
The JSON must be valid and complete."""


async def schema_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /schema <url> command."""
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a URL.\nUsage: `/schema https://example.com/page`",
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

    await update.message.reply_text(f"🔍 Analysing `{url}` …", parse_mode="Markdown")

    # Gather page data
    metadata = get_page_metadata(url)
    page_text = fetch_page_text(url)

    if not metadata and not page_text:
        await update.message.reply_text(
            "❌ Could not fetch the page. Please check the URL and try again."
        )
        return

    meta_str = json.dumps(metadata or {}, ensure_ascii=False, indent=2)
    user_message = (
        f"URL: {url}\n\n"
        f"Page metadata:\n{meta_str}\n\n"
        f"Page text (first 3 000 chars):\n{page_text}"
    )

    try:
        schema_json = ask_claude(SYSTEM_PROMPT, user_message)
        # Validate that Claude returned parseable JSON
        json.loads(schema_json)

        reply = (
            f"✅ *SEO JSON-LD Schema* for `{url}`\n\n"
            f"```json\n{schema_json}\n```"
        )
        await update.message.reply_text(
            reply, parse_mode="Markdown", disable_web_page_preview=True
        )
    except json.JSONDecodeError:
        logger.warning("Claude returned non-JSON schema response")
        await update.message.reply_text(
            f"🧠 *Claude's schema suggestion:*\n\n{schema_json}",
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )
    except Exception as exc:
        logger.error("Schema handler error: %s", exc)
        await update.message.reply_text(
            "❌ An error occurred while generating the schema. Please try again later."
        )
