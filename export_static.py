"""
export_static.py
Exports the latest curated digest to frontend/data/news.json
so GitHub Pages can serve it as a static file.

Run after run_curate.py:
    python export_static.py
"""
import json
import os
from datetime import datetime, timezone
from app.services.digest_store import get_digest

def export():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest = get_digest(today)

    if not digest:
        print(f"No digest found for {today}. Run run_curate.py first.")
        return

    # Inject audio URL for GitHub Pages (Voice Assistant fallback)
    github_pages_base = os.getenv(
        "GITHUB_PAGES_BASE_URL",
        "https://mayank-goyal09.github.io/news-curator"
    )
    audio_file = f"data/audio/digest_{today}.mp3"
    if os.path.exists(audio_file):
        digest["audio_url"] = f"{github_pages_base.rstrip('/')}/{audio_file}"

    out_dir = os.path.join("frontend", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "news.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(digest, f, ensure_ascii=False, indent=2)

    cats = digest.get("categories", {})
    total = sum(len(v) for v in cats.values())
    rec   = len(digest.get("recommended", []))
    print(f"✅ Exported {total} articles + {rec} recommended → {out_path}")
    print(f"   Date: {today}")
    if digest.get("audio_url"):
        print(f"   🎧 Audio: {digest['audio_url']}")

if __name__ == "__main__":
    export()
