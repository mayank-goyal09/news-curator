# app/main.py
from fastapi import FastAPI
from app.routers import health, digests
from app.db.sqlite import init_db

app = FastAPI(title="AI News Curator")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(health.router)
app.include_router(digests.router)
