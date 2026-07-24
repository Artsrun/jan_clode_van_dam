"""Main entry point for the Telegram bot."""

import logging

from telegram import BotCommand
from telegram.ext import Application, CommandHandler

import config  # noqa: F401 – triggers env-var loading & logging setup
from config import TELEGRAM_BOT_TOKEN
from handlers.start import start_handler, help_handler
from handlers.schema import schema_handler
from handlers.feed import feed_handler
from handlers.forums import forums_handler

logger = logging.getLogger(__name__)


async def _post_init(application: Application) -> None:
    """Register bot commands in the Telegram menu after startup."""
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Introduction & usage guide"),
            BotCommand("help", "Show available commands"),
            BotCommand("schema", "Generate SEO JSON-LD schema for a URL"),
            BotCommand("feed", "Fetch & summarise an RSS/Atom tech feed"),
            BotCommand("forums", "Analyse tech forum discussions on a topic"),
        ]
    )
    logger.info("Bot commands registered.")


def main() -> None:
    """Build and run the Telegram bot."""
    logger.info("Starting Claude AI Telegram Bot …")

    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(_post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("schema", schema_handler))
    application.add_handler(CommandHandler("feed", feed_handler))
    application.add_handler(CommandHandler("forums", forums_handler))

    logger.info("Polling for updates …")
    application.run_polling()


if __name__ == "__main__":
    main()
