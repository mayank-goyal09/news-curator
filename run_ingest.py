# run_ingest.py
from app.core.sources import SOURCES
from app.services.fetcher import fetch_feed
from app.db.sqlite import init_db, get_conn

def save_articles(rows, category=""):
    with get_conn() as conn:
        for a in rows:
            conn.execute(
                """
                INSERT OR IGNORE INTO articles(source_id, category, title, url, published_at, summary, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (a.source_id, category, a.title, a.url, a.published_at, a.summary, a.image_url),
            )

def main():
    init_db()

    all_articles = []
    for s in SOURCES:
        articles = fetch_feed(s["id"], s["feed_url"], limit=20)
        category = s.get("category", "")
        save_articles(articles, category=category)
        all_articles.extend(articles)

    print(f"\nSaved (deduped) total fetched: {len(all_articles)}")

if __name__ == "__main__":
    main()
