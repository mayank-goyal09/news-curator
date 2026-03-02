# app/main.py
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.db.sqlite import init_db, get_conn
from app.routers import health, digests
from app.services.digest_store import get_digest
from app.core.sources import CATEGORIES

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="AI News Curator")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(health.router)
app.include_router(digests.router)


# ─── API ENDPOINTS ───────────────────────────────────────────────────

@app.get("/api/categories")
def get_categories():
    """Return category metadata."""
    cats = {}
    for key, data in CATEGORIES.items():
        cats[key] = {"label": data["label"], "source_count": len(data["sources"])}
    return {"categories": cats}


@app.get("/api/news")
def get_news(category: str = None):
    """
    Return curated news from the latest digest.
    If category is specified, return only that category's news.
    Otherwise return all categories.
    """
    date = datetime.now(timezone.utc).date().isoformat()
    digest = get_digest(date)

    if not digest:
        # Try yesterday
        from datetime import timedelta
        yesterday = (datetime.now(timezone.utc).date() - timedelta(days=1)).isoformat()
        digest = get_digest(yesterday)

    if not digest:
        # Try to find the latest digest in the database
        with get_conn() as conn:
            row = conn.execute(
                "SELECT payload_json FROM digests ORDER BY date_utc DESC LIMIT 1"
            ).fetchone()
        if row:
            import json
            digest = json.loads(row["payload_json"])

    if not digest:
        # Return empty structure
        return {
            "date": date,
            "overall_summary": "No digest available yet. Run the pipeline first.",
            "categories": {k: [] for k in CATEGORIES},
            "audio_url": None,
        }

    # Build response
    categories_data = digest.get("categories", {})

    # If old format (top_picks only), convert
    if not categories_data and digest.get("top_picks"):
        categories_data = {"satire": [], "ai": [], "worldwide": [], "warming": [], "market": []}
        for pick in digest["top_picks"]:
            cat = pick.get("category", "ai")
            if cat in categories_data:
                categories_data[cat].append(pick)

    if category and category in categories_data:
        filtered = {category: categories_data[category]}
    elif category:
        filtered = {category: []}
    else:
        filtered = categories_data

    return {
        "date": digest.get("date_utc", date),
        "overall_summary": digest.get("overall_summary", ""),
        "categories": filtered,
        "recommended": digest.get("recommended", []),
        "audio_url": digest.get("audio_url", None),
    }


@app.get("/api/news/featured")
def get_featured_news():
    """Return the single featured 'best of the week' article."""
    date = datetime.now(timezone.utc).date().isoformat()
    digest = get_digest(date)

    if not digest:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT payload_json FROM digests ORDER BY date_utc DESC LIMIT 1"
            ).fetchone()
        if row:
            import json
            digest = json.loads(row["payload_json"])

    if not digest:
        return {
            "title": "Welcome to EcoNews",
            "meta": "News Curator • Just launched",
            "why_pick": "Your personalized news digest is being prepared. Run the pipeline to see curated news.",
            "tags": ["news", "ai"],
            "url": "#",
        }

    # Pick the first item overall as featured
    all_picks = digest.get("top_picks", [])
    if not all_picks:
        cats = digest.get("categories", {})
        for cat_items in cats.values():
            all_picks.extend(cat_items)

    if all_picks:
        featured = all_picks[0]
        return {
            "title": featured.get("title", ""),
            "meta": f"{featured.get('source_id', 'News')} • Today",
            "why_pick": featured.get("why_pick", ""),
            "tags": featured.get("tags", []),
            "url": featured.get("url", "#"),
            "image_url": featured.get("image_url"),
        }

    return {
        "title": "No featured article yet",
        "meta": "EcoNews",
        "why_pick": "Run the pipeline to curate news.",
        "tags": [],
        "url": "#",
    }


@app.get("/api/audio")
def get_audio():
    """Return the audio URL for the latest digest."""
    date = datetime.now(timezone.utc).date().isoformat()
    digest = get_digest(date)

    if not digest:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT payload_json FROM digests ORDER BY date_utc DESC LIMIT 1"
            ).fetchone()
        if row:
            import json
            digest = json.loads(row["payload_json"])

    audio_url = digest.get("audio_url") if digest else None

    # Also check local file
    audio_dir = BASE_DIR / "data" / "audio"
    local_files = sorted(audio_dir.glob("digest_*.mp3"), reverse=True) if audio_dir.exists() else []
    local_path = f"/audio/{local_files[0].name}" if local_files else None

    return {
        "audio_url": audio_url,
        "local_audio": local_path,
    }


class SubscribeRequest(BaseModel):
    email: str

@app.post("/api/subscribe")
def subscribe(req: SubscribeRequest):
    """Subscribe an email to the newsletter."""
    email = req.email.strip().lower()
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email address")

    with get_conn() as conn:
        try:
            conn.execute(
                "INSERT INTO subscribers(email) VALUES (?)",
                (email,),
            )
        except Exception:
            pass  # Already subscribed

    return {"status": "subscribed", "email": email}


@app.get("/api/subscribers")
def list_subscribers():
    """List all subscribers (for admin use)."""
    with get_conn() as conn:
        rows = conn.execute("SELECT email, subscribed_at FROM subscribers ORDER BY subscribed_at DESC").fetchall()
    return {"subscribers": [dict(r) for r in rows]}


# ─── SERVE LOCAL AUDIO FILES ────────────────────────────────────────

audio_dir = BASE_DIR / "data" / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")


# ─── SERVE FRONTEND ─────────────────────────────────────────────────

@app.get("/")
def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

# Mount frontend static files (CSS, JS, images)
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")
