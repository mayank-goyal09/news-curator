# app/services/tts.py
from pathlib import Path
import pyttsx3

CATEGORY_LABELS = {
    "satire": "Satire",
    "ai": "AI Technology",
    "worldwide": "Worldwide News",
    "warming": "Warming and Emotions",
    "market": "Market News",
}

def digest_to_text(digest: dict) -> str:
    lines = []
    lines.append(f"Daily Tech Digest. Date {digest.get('date_utc','')}")
    if digest.get("overall_summary"):
        lines.append(digest["overall_summary"])

    # Try categorized format first
    categories = digest.get("categories", {})
    if categories:
        for cat_key in ["satire", "ai", "worldwide", "warming", "market"]:
            cat_items = categories.get(cat_key, [])
            if not cat_items:
                continue
            cat_label = CATEGORY_LABELS.get(cat_key, cat_key)
            lines.append(f"\n{cat_label} Section.")
            for i, item in enumerate(cat_items, start=1):
                lines.append(f"Item {i}. {item.get('title','')}")
                lines.append(item.get("why_pick", ""))
    else:
        # Fallback to flat top_picks
        for i, item in enumerate(digest.get("top_picks", []), start=1):
            lines.append(f"Item {i}. {item.get('title','')}")
            lines.append(item.get("why_pick", ""))

    text = "\n".join([x.strip() for x in lines if x and x.strip()])
    return text

def generate_audio(digest: dict, out_path: str) -> str:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    text = digest_to_text(digest)

    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.save_to_file(text, str(out))
    engine.runAndWait()

    return str(out)
