# app/services/curator.py
import json
from app.services.ollama_client import ollama_generate_json

CURATION_SCHEMA = {
  "type": "object",
  "properties": {
    "date_utc": {"type": "string"},
    "overall_summary": {"type": "string"},
    "top_picks": {
      "type": "array",
      "minItems": 5,
      "maxItems": 5,
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
  "required": ["date_utc", "overall_summary", "top_picks"]
}



def build_prompt(articles):
    return (
        "You are a senior engineer curating a daily tech digest.\n"
        "Return ONLY JSON that matches the schema.\n"
        "Requirements:\n"
        "- date_utc: YYYY-MM-DD\n"
        "- overall_summary: 3 to 5 sentences summarizing today's themes\n"
        "- top_picks: EXACTLY 5 items\n"
        "- why_pick: 1 to 2 specific sentences (no generic fluff)\n"
        "- tags: 2 to 4 short lowercase tags\n\n"
        f"ARTICLES:\n{json.dumps(articles, ensure_ascii=False)}"
    )




def curate(articles: list[dict]) -> dict:
    prompt = build_prompt(articles)
    raw = ollama_generate_json(prompt, schema=CURATION_SCHEMA)
    print("RAW MODEL RESPONSE TEXT:\n", raw["response"][:500])
    return json.loads(raw["response"])

