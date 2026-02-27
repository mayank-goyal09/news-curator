# run_send_email.py
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

from app.db.sqlite import init_db
from app.services.digest_store import get_digest
from app.services.email_renderer import render_digest_html
from app.services.email_sender import send_email_html


def main():
    init_db()

    # ✅ Auto date (UTC) to match your stored digest key format
    date = datetime.now(timezone.utc).date().isoformat()

    digest = get_digest(date)
    if not digest:
        raise SystemExit(f"No digest found for {date}. Run run_curate.py first.")

    html = render_digest_html(digest)
    send_email_html(subject=f"Daily Tech Digest — {date}", html=html)
    print("Email sent successfully.")


if __name__ == "__main__":
    main()
