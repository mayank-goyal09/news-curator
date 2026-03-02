# run_curate.py
from datetime import datetime
from app.db.sqlite import init_db, get_conn
from app.services.curator import curate
from app.services.digest_store import save_digest


def load_latest_by_category(per_category: int = 10):
    """Load latest articles grouped by category for curation."""
    categories = ["satire", "ai", "worldwide", "warming", "market"]
    result = {}
    with get_conn() as conn:
        for cat in categories:
            rows = conn.execute(
                """
                SELECT source_id, title, url, published_at, image_url
                FROM articles
                WHERE category = ?
                ORDER BY COALESCE(published_at, fetched_at) DESC
                LIMIT ?
                """,
                (cat, per_category),
            ).fetchall()
            result[cat] = [dict(r) for r in rows]
    return result


def main():
    init_db()
    articles_by_cat = load_latest_by_category(10)
    
    # Show what we have
    for cat, arts in articles_by_cat.items():
        print(f"Category '{cat}': {len(arts)} articles available")

    result = curate(articles_by_cat)

    # Normalize date
    dt = datetime.fromisoformat(result["date_utc"])
    result["date_utc"] = dt.date().isoformat()

    save_digest(result["date_utc"], result)
    print("Saved digest for:", result["date_utc"])
    
    # Summary
    cats = result.get("categories", {})
    total = sum(len(v) for v in cats.values())
    print(f"Total curated items: {total}")
    for cat, items in cats.items():
        print(f"  {cat}: {len(items)} items")


if __name__ == "__main__":
    main()
