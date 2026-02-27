from datetime import datetime
from app.db.sqlite import init_db, get_conn
from app.services.curator import curate
from app.services.digest_store import save_digest


def load_latest(limit: int = 30):
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT source_id, title, url, published_at
            FROM articles
            ORDER BY COALESCE(published_at, fetched_at) DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def main():
    init_db()
    articles = load_latest(30)
    result = curate(articles)

    # ✅ FIX: normalize to YYYY-MM-DD BEFORE saving
    # If Ollama returns ISO datetime like "2025-12-25T13:02:46+00:00"
    dt = datetime.fromisoformat(result["date_utc"])
    result["date_utc"] = dt.date().isoformat()  # "YYYY-MM-DD"

    save_digest(result["date_utc"], result)
    print("Saved digest for:", result["date_utc"])
    print(result)


if __name__ == "__main__":
    main()
