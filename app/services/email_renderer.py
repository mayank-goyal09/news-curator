# app/services/email_renderer.py
from html import escape

CATEGORY_LABELS = {
    "satire": "🎭 Satire",
    "ai": "🤖 AI Technology",
    "worldwide": "🌍 Worldwide News",
    "warming": "💛 Warming & Emotions",
    "market": "📈 Market News",
}

def _clean(s: str) -> str:
    return (s or "").replace("\xa0", " ")


def render_digest_html(digest: dict) -> str:
    date = escape(_clean(digest.get("date_utc", "")))
    summary = escape(_clean(digest.get("overall_summary", "")))

    # Audio section
    audio_html = ""
    audio_url = digest.get("audio_url")
    if audio_url:
        audio_html = f"""
        <div style="margin-bottom: 20px; padding: 10px; background-color: #f1f5f9; border-radius: 8px;">
            <strong style="display:block; margin-bottom: 8px; color: #1e293b;">🎧 Listen to today's digest:</strong>
            <audio controls style="width: 100%; max-width: 400px;">
                <source src="{audio_url}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <div style="margin-top: 8px; font-size: 12px;">
                <a href="{audio_url}" target="_blank" style="color: #3b82f6; text-decoration: none;">Download / Open Audio in Browser</a>
            </div>
        </div>
        """

    # Build categorized sections
    categories_html = []
    categories = digest.get("categories", {})
    
    # Fallback to old format
    if not categories and digest.get("top_picks"):
        categories = {"highlights": digest["top_picks"]}

    for cat_key in ["satire", "ai", "worldwide", "warming", "market"]:
        items = categories.get(cat_key, [])
        if not items:
            continue
        
        label = CATEGORY_LABELS.get(cat_key, cat_key.title())
        items_html = []
        for i, item in enumerate(items, start=1):
            title = escape(_clean(item.get("title", "")))
            url = item.get("url", "")
            why = escape(_clean(item.get("why_pick", "")))
            tags = ", ".join(item.get("tags", []))
            tags = escape(_clean(tags))

            img_html = ""
            image_url = item.get("image_url")
            if image_url:
                img_html = f'<div style="margin-top: 8px; margin-bottom: 8px;"><img src="{image_url}" style="max-width: 100%; max-height: 200px; border-radius: 4px;" alt="Article Image"/></div>'

            items_html.append(f"""
            <li style="margin-bottom:16px;">
              <div><b><a href="{url}" style="color: #1C5D42; text-decoration: none;">{title}</a></b></div>
              {img_html}
              <div style="margin-top: 4px; color: #333;">{why}</div>
              <div style="color:#888;font-size:12px;">Tags: {tags}</div>
            </li>
            """)

        categories_html.append(f"""
        <div style="margin-bottom: 24px;">
            <h3 style="color: #123C2A; border-bottom: 2px solid #E7F3EE; padding-bottom: 8px; margin-bottom: 12px;">{label}</h3>
            <ul style="padding-left: 20px;">
                {''.join(items_html)}
            </ul>
        </div>
        """)

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto; padding: 20px; background-color: #FDFBF5;">
        <div style="text-align: center; margin-bottom: 24px;">
            <div style="display: inline-block; width: 20px; height: 20px; background: linear-gradient(135deg, #31A572, #123C2A); border-radius: 4px; transform: rotate(45deg); margin-bottom: 8px;"></div>
            <h1 style="color: #0D2017; margin: 8px 0;">EcoNews Daily Digest</h1>
            <p style="color: #587164;">{date}</p>
        </div>
        {audio_html}
        <div style="background: #E7F3EE; border-radius: 12px; padding: 16px; margin-bottom: 24px;">
            <p style="color: #1C5D42; margin: 0;">{summary}</p>
        </div>
        {''.join(categories_html)}
        <div style="text-align: center; color: #9BB0A5; font-size: 12px; margin-top: 32px; padding-top: 16px; border-top: 1px solid #EAEAE0;">
            <p>EcoNews — AI-Curated Daily Digest</p>
        </div>
      </body>
    </html>
    """
