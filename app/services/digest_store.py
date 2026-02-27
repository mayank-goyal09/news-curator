# app/services/digest_store.py
import json
from app.db.sqlite import get_conn

def save_digest(date_utc: str, payload: dict) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO digests(date_utc, payload_json)
            VALUES (?, ?)
            """,
            (date_utc, json.dumps(payload, ensure_ascii=False)),
        )

def get_digest(date_utc: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT payload_json FROM digests WHERE date_utc = ?",
            (date_utc,),
        ).fetchone()
    return json.loads(row["payload_json"]) if row else None
