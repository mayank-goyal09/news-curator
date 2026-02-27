# app/services/email_renderer.py
from html import escape


def _clean(s: str) -> str:
    # Replace non‑breaking spaces with normal spaces
    return (s or "").replace("\xa0", " ")


def render_digest_html(digest: dict) -> str:
    date = escape(_clean(digest.get("date_utc", "")))
    summary = escape(_clean(digest.get("overall_summary", "")))

    items_html = []
    for i, item in enumerate(digest.get("top_picks", []), start=1):
        title = escape(_clean(item.get("title", "")))
        url = item.get("url", "")
        why = escape(_clean(item.get("why_pick", "")))

        tags = ", ".join(item.get("tags", []))
        tags = escape(_clean(tags))

        items_html.append(
            f"""
            <li style="margin-bottom:16px;">
              <div><b>{i}. <a href="{url}">{title}</a></b></div>
              <div>{why}</div>
              <div style="color:#666;font-size:12px;">Tags: {tags}</div>
            </li>
            """
        )

    audio_html = ""
    audio_url = digest.get("audio_url")
    if audio_url:
        audio_html = f"""
        <div style="margin-bottom: 20px; padding: 10px; background-color: #f1f5f9; border-radius: 8px;">
            <strong style="display:block; margin-bottom: 8px; color: #1e293b;">Listen to today's digest:</strong>
            <audio controls style="width: 100%; max-width: 400px;">
                <source src="{audio_url}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <div style="margin-top: 8px; font-size: 12px;">
                <a href="{audio_url}" target="_blank" style="color: #3b82f6; text-decoration: none;">Download / Open Audio in Browser</a>
            </div>
        </div>
        """

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2>Daily Tech Digest — {date}</h2>
        {audio_html}
        <p>{summary}</p>
        <ol>
          {''.join(items_html)}
        </ol>
      </body>
    </html>
    """
