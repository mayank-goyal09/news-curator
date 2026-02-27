# app/routers/digests.py
from fastapi import APIRouter, HTTPException
from app.services.digest_store import get_digest

router = APIRouter(prefix="/digests", tags=["digests"])

@router.get("/{date_utc}")
def read_digest(date_utc: str):
    digest = get_digest(date_utc)
    if not digest:
        raise HTTPException(status_code=404, detail="Digest not found")
    return digest
