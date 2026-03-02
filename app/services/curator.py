# app/services/curator.py
import json
from app.services.ollama_client import ollama_generate_json

# Simple schema per category (what we KNOW llama3.2 can handle)
CATEGORY_SCHEMA = {
  "type": "object",
  "properties": {
    "picks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": {"type": "string"},
          "url": {"type": "string"},
          "source_id": {"type": "string"},
          "why_pick": {"type": "string"},
          "tags": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["title", "url", "source_id", "why_pick", "tags"]
      }
    }
  },
  "required": ["picks"]
}

SUMMARY_SCHEMA = {
  "type": "object",
  "properties": {
    "date_utc": {"type": "string"},
    "overall_summary": {"type": "string"}
  },
  "required": ["date_utc", "overall_summary"]
}

CATEGORY_LABELS = {
    "satire": "Satire & Humor",
    "ai": "AI & Technology",
    "worldwide": "World News",
    "warming": "Heartwarming & Emotional",
    "market": "Market & Finance",
}


def build_category_prompt(category_label: str, articles: list, count: int = 4) -> str:
    return (
        f"You are a news editor curating the best {category_label} stories.\n"
        "Return ONLY JSON matching the schema.\n"
        f"Pick EXACTLY {count} most interesting articles from the list below.\n"
        "For each pick:\n"
        "- title: the article title\n"
        "- url: the article URL\n"
        "- source_id: the source\n"
        "- why_pick: 1-2 specific sentences about WHY this article matters\n"
        "- tags: 2-4 short lowercase tags\n\n"
        f"ARTICLES:\n{json.dumps(articles, ensure_ascii=False)}"
    )


def build_summary_prompt(all_titles: list) -> str:
    return (
        "You are a senior editor writing a daily news digest summary.\n"
        "Return ONLY JSON. Fields: date_utc (YYYY-MM-DD), overall_summary (3-5 sentences).\n"
        "Summarize the themes across these headlines:\n"
        + "\n".join(f"- {t}" for t in all_titles)
    )


def curate_category(category: str, articles: list, count: int = 4) -> list:
    """Curate a single category. Returns list of picks."""
    if not articles:
        return []

    label = CATEGORY_LABELS.get(category, category)
    prompt = build_category_prompt(label, articles, count)

    try:
        raw = ollama_generate_json(prompt, schema=CATEGORY_SCHEMA)
        print(f"  [{category}] raw response (first 300 chars): {raw['response'][:300]}")
        result = json.loads(raw["response"])
        picks = result.get("picks", [])
        return picks[:count]
    except Exception as e:
        print(f"  [{category}] curation failed: {e}")
        # Fallback: use first N articles as-is
        return [
            {
                "title": a.get("title", ""),
                "url": a.get("url", ""),
                "source_id": a.get("source_id", ""),
                "why_pick": f"Selected from {label} feed.",
                "tags": [category],
            }
            for a in articles[:count]
        ]


def curate(articles_by_category: dict) -> dict:
    """
    Curate each category separately for reliability.
    articles_by_category: {"satire": [...], "ai": [...], ...}
    """
    # Target: 3 per category (15) + 6 recommended sidebar = 21 total
    counts = {"satire": 3, "ai": 3, "worldwide": 3, "warming": 3, "market": 3}

    categories_result = {}
    all_titles = []
    used_urls = set()

    for cat_key in ["satire", "ai", "worldwide", "warming", "market"]:
        cat_articles = articles_by_category.get(cat_key, [])
        target_count = counts.get(cat_key, 3)
        print(f"\nCurating '{cat_key}' ({len(cat_articles)} articles → {target_count} picks)...")
        
        picks = curate_category(cat_key, cat_articles, target_count)

        # Attach images deterministically
        url_to_image = {a["url"]: a.get("image_url") for a in cat_articles if a.get("image_url")}
        for pick in picks:
            pick_url = pick.get("url", "")
            if pick_url in url_to_image:
                pick["image_url"] = url_to_image[pick_url]
            else:
                for art_url, img in url_to_image.items():
                    if art_url in pick_url or pick_url in art_url:
                        pick["image_url"] = img
                        break
            pick["category"] = cat_key
            used_urls.add(pick.get("url", ""))

        categories_result[cat_key] = picks
        all_titles.extend([p.get("title", "") for p in picks])

    # Build 6 "recommended" sidebar items from leftover articles across categories
    recommended = []
    for cat_key in ["ai", "market", "worldwide", "satire", "warming"]:
        cat_articles = articles_by_category.get(cat_key, [])
        for a in cat_articles:
            if a.get("url") not in used_urls and len(recommended) < 6:
                recommended.append({
                    "title": a.get("title", ""),
                    "url": a.get("url", ""),
                    "source_id": a.get("source_id", ""),
                    "why_pick": f"Recommended from {CATEGORY_LABELS.get(cat_key, cat_key)}.",
                    "tags": [cat_key],
                    "category": cat_key,
                    "image_url": a.get("image_url"),
                })
                used_urls.add(a.get("url"))

    # Generate overall summary
    print("\nGenerating overall summary...")
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).date().isoformat()
    try:
        summary_raw = ollama_generate_json(build_summary_prompt(all_titles), schema=SUMMARY_SCHEMA)
        summary_data = json.loads(summary_raw["response"])
    except Exception as e:
        print(f"Summary generation failed: {e}")
        summary_data = {
            "date_utc": today,
            "overall_summary": "Today's digest covers stories across technology, world news, markets, and more.",
        }

    # Build flat list for backward compat
    all_picks = []
    for cat_key in ["satire", "ai", "worldwide", "warming", "market"]:
        all_picks.extend(categories_result.get(cat_key, []))

    return {
        "date_utc": today,  # Always use real today's date
        "overall_summary": summary_data.get("overall_summary", ""),
        "categories": categories_result,
        "recommended": recommended,
        "top_picks": all_picks,
    }
