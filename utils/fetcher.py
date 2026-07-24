"""Web-content fetching utilities (RSS feeds, HTML pages)."""

import logging
from typing import Optional
from urllib.parse import urlparse

import feedparser
import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; TelegramBot/1.0; "
        "+https://github.com/Artsrun/jan_clode_van_dam)"
    )
}


# ── Feed helpers ─────────────────────────────────────────────────────────────

def fetch_feed(url: str, max_entries: int = 5) -> list[dict]:
    """Parse an RSS/Atom feed and return a list of entry dicts.

    Each dict has keys: title, link, summary, published.

    Args:
        url:         RSS or Atom feed URL.
        max_entries: Maximum number of entries to return.

    Returns:
        List of entry dictionaries (may be empty on failure).
    """
    logger.info("Fetching feed: %s", url)
    try:
        parsed = feedparser.parse(url, request_headers=HEADERS)
        entries = []
        for entry in parsed.entries[:max_entries]:
            entries.append(
                {
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "summary": _clean_html(entry.get("summary", "")),
                    "published": entry.get("published", ""),
                }
            )
        return entries
    except Exception as exc:
        logger.error("Feed fetch error for %s: %s", url, exc)
        return []


# ── HTML helpers ─────────────────────────────────────────────────────────────

def fetch_page_text(url: str, max_chars: int = 3000) -> str:
    """Fetch a web page and return its visible text content (truncated).

    Args:
        url:       The page URL.
        max_chars: Maximum characters of text to return.

    Returns:
        Visible text from the page, or an empty string on failure.
    """
    logger.info("Fetching page: %s", url)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return _clean_html(resp.text)[:max_chars]
    except requests.RequestException as exc:
        logger.error("Page fetch error for %s: %s", url, exc)
        return ""


def _clean_html(raw: str) -> str:
    """Strip HTML tags and collapse whitespace."""
    soup = BeautifulSoup(raw, "lxml")
    text = soup.get_text(separator=" ")
    return " ".join(text.split())


# ── URL validation ────────────────────────────────────────────────────────────

def is_valid_url(url: str) -> bool:
    """Return True if *url* has a valid scheme and netloc."""
    try:
        result = urlparse(url)
        return result.scheme in ("http", "https") and bool(result.netloc)
    except ValueError:
        return False


def get_page_metadata(url: str) -> Optional[dict]:
    """Fetch Open Graph / standard meta tags from a URL.

    Returns a dict with keys: title, description, url, image, site_name.
    Returns None on failure.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        def og(prop: str) -> str:
            tag = soup.find("meta", property=f"og:{prop}") or soup.find(
                "meta", attrs={"name": f"og:{prop}"}
            )
            return tag["content"].strip() if tag and tag.get("content") else ""

        title = (
            og("title")
            or (soup.title.string.strip() if soup.title else "")
        )
        description = og("description") or (
            (soup.find("meta", attrs={"name": "description"}) or {}).get(
                "content", ""
            )
        )

        return {
            "title": title,
            "description": description,
            "url": og("url") or url,
            "image": og("image"),
            "site_name": og("site_name"),
        }
    except Exception as exc:
        logger.error("Metadata fetch error for %s: %s", url, exc)
        return None
