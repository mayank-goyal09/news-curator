# app/services/fetcher.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import feedparser


@dataclass
class Article:
    source_id: str
    title: str
    url: str
    published_at: str | None
    summary: str | None
    image_url: str | None


def _to_iso8601(entry: Any) -> str | None:
    # feedparser often provides structured_time in 'published_parsed' or 'updated_parsed'
    for key in ("published_parsed", "updated_parsed"):
        st = getattr(entry, key, None)
        if st:
            dt = datetime(*st[:6], tzinfo=timezone.utc)
            return dt.isoformat()
    return None


def _get_summary(entry: Any) -> str | None:
    # Some feeds provide summary, some provide content
    summary = getattr(entry, "summary", None)
    if summary:
        return summary
    content = getattr(entry, "content", None)
    if content and isinstance(content, list) and len(content) > 0:
        return content[0].get("value")
    return None


import re

def _get_image(entry: Any) -> str | None:
    # Check media_content
    media_content = getattr(entry, "media_content", None)
    if media_content and isinstance(media_content, list) and len(media_content) > 0:
        url = media_content[0].get("url")
        if url: return url

    # Check media_thumbnail
    media_thumbnail = getattr(entry, "media_thumbnail", None)
    if media_thumbnail and isinstance(media_thumbnail, list) and len(media_thumbnail) > 0:
        url = media_thumbnail[0].get("url")
        if url: return url

    # Check links (rel="enclosure" or type="image/*")
    links = getattr(entry, "links", [])
    for link in links:
        if link.get("type", "").startswith("image/") or link.get("rel") == "enclosure":
            url = link.get("href")
            if url: return url

    # Fallback: Scrape from summary or content using regex
    html_corpus = getattr(entry, "summary", "")
    content_list = getattr(entry, "content", [])
    for c in content_list:
        html_corpus += " " + c.get("value", "")

    if html_corpus:
        # Match <img ... src="url" ...>
        match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html_corpus, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def fetch_feed(source_id: str, feed_url: str, limit: int = 20) -> list[Article]:
    parsed = feedparser.parse(feed_url)

    # Debug: show what feedparser thinks
    print(f"\n[{source_id}] url={feed_url}")
    print(f"[{source_id}] bozo={getattr(parsed, 'bozo', None)} entries={len(getattr(parsed, 'entries', []))}")

    if getattr(parsed, "bozo", 0):
        print(f"[{source_id}] bozo_exception={getattr(parsed, 'bozo_exception', None)}")

    articles: list[Article] = []
    for entry in parsed.entries[:limit]:
        title = (getattr(entry, "title", "") or "").strip()
        url = (getattr(entry, "link", "") or "").strip()

        # Debug if missing
        if not title or not url:
            print(f"[{source_id}] skipped entry missing title/url")
            continue

        articles.append(
            Article(
                source_id=source_id,
                title=title,
                url=url,
                published_at=_to_iso8601(entry),
                summary=_get_summary(entry),
                image_url=_get_image(entry),
            )
        )

    return articles
