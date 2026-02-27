# run_tts.py
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from datetime import datetime, timezone
from app.db.sqlite import init_db
from app.services.digest_store import get_digest, save_digest
from app.services.tts import generate_audio
from app.services.github_uploader import upload_audio_to_github

def main():
    init_db()
    date = datetime.now(timezone.utc).date().isoformat()
    digest = get_digest(date)
    if not digest:
        raise SystemExit(f"No digest found for {date}. Run run_curate.py first.")

    audio_path = generate_audio(digest, f"data/audio/digest_{date}.mp3")
    print("Audio generated:", audio_path)

    # Upload to github
    public_url = upload_audio_to_github(audio_path)
    if public_url:
        digest["audio_url"] = public_url
        save_digest(date, digest)
        print("Updated digest with public audio URL:", public_url)

if __name__ == "__main__":
    main()
