# app/services/tts.py
from pathlib import Path
import pyttsx3

def digest_to_text(digest: dict) -> str:
    lines = []
    lines.append(f"Daily Tech Digest. Date {digest.get('date_utc','')}.")
    if digest.get("overall_summary"):
        lines.append(digest["overall_summary"])

    for i, item in enumerate(digest.get("top_picks", []), start=1):
        lines.append(f"Item {i}. {item.get('title','')}.")
        lines.append(item.get("why_pick", ""))

    # Clean extra spaces
    text = "\n".join([x.strip() for x in lines if x and x.strip()])
    return text

def generate_audio(digest: dict, out_path: str) -> str:
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    text = digest_to_text(digest)

    engine = pyttsx3.init()
    engine.setProperty("rate", 175)  # optional: adjust speed
    engine.save_to_file(text, str(out))
    engine.runAndWait()

    return str(out)
