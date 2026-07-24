"""Claude AI client wrapper."""

import logging
from typing import Optional

import anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, CLAUDE_MAX_TOKENS

logger = logging.getLogger(__name__)

_client: Optional[anthropic.Anthropic] = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def ask_claude(system_prompt: str, user_message: str) -> str:
    """Send a message to Claude and return the text response.

    Args:
        system_prompt: Instruction that shapes Claude's behaviour.
        user_message:  The user-facing content to process.

    Returns:
        The assistant's text reply.

    Raises:
        anthropic.APIError: On upstream API failures.
    """
    client = _get_client()
    logger.debug("Sending request to Claude model=%s", CLAUDE_MODEL)

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    text = response.content[0].text
    logger.debug("Claude response received (%d chars)", len(text))
    return text
