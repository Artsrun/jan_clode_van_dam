"""Telegram /start and /help command handlers."""

from telegram import Update
from telegram.ext import ContextTypes

HELP_TEXT = """
🤖 *Claude AI · Tech Forum & SEO Bot*

I use Anthropic's Claude AI to help you analyse tech forum content and generate SEO assets.

*Commands:*

/schema `<url>` – Generate JSON-LD SEO Schema markup for any URL.
/feed `<url>` – Fetch & summarise an RSS/Atom tech feed.
/forums `<topic>` – Find & analyse tech forum discussions on a topic.

*Examples:*
• `/schema https://example.com/article`
• `/feed https://feeds.feedburner.com/TechCrunch`
• `/forums Python asyncio best practices`

Powered by [Claude AI](https://www.anthropic.com) 🧠
""".strip()


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    await update.message.reply_text(
        f"👋 Hello, {update.effective_user.first_name}!\n\n{HELP_TEXT}",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
