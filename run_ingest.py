from app.core.sources import SOURCES
from app.services.fetcher import fetch_feed
from app.db.sqlite import init_db, get_conn

def save_articles(rows):
    with get_conn() as conn:
        for a in rows:
            conn.execute(
                """
                INSERT OR IGNORE INTO articles(source_id, title, url, published_at, summary)
                VALUES (?, ?, ?, ?, ?)
                """,
                (a.source_id, a.title, a.url, a.published_at, a.summary),
            )

def main():
    init_db()

    all_articles = []
    for s in SOURCES:
        articles = fetch_feed(s["id"], s["feed_url"], limit=20)
        all_articles.extend(articles)

    save_articles(all_articles)

    print(f"\nSaved (deduped) total fetched: {len(all_articles)}")

if __name__ == "__main__":
    main()

