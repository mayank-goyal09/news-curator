# app/services/email_sender.py
import os
import smtplib
from email.message import EmailMessage


def _clean(s: str) -> str:
    # Normalize non-breaking spaces and strip
    return (s or "").replace("\xa0", " ").strip()


def _get_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing environment variable: {name}")
    return _clean(val)


def send_email_html(subject: str, html: str, to_override: str = None) -> None:
    sender = _get_env("NEWS_EMAIL_SENDER")
    to_addr = to_override or _get_env("NEWS_EMAIL_TO")

    # App password: remove spaces completely (Google shows it in groups)
    app_password = _get_env("NEWS_EMAIL_APP_PASSWORD").replace(" ", "")

    subject = _clean(subject)
    html = _clean(html)

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_addr
    msg["Subject"] = subject

    # Plain fallback + HTML alternative
    msg.set_content("Your email client does not support HTML.")
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        if os.getenv("NEWS_EMAIL_DEBUG") == "1":
            smtp.set_debuglevel(1)
        smtp.login(sender, app_password)
        smtp.send_message(msg)


def send_to_all_subscribers(subject: str, html: str) -> int:
    """Send digest email to all subscribers. Returns count of emails sent."""
    from app.db.sqlite import get_conn
    
    with get_conn() as conn:
        rows = conn.execute("SELECT email FROM subscribers").fetchall()
    
    sent_count = 0
    for row in rows:
        try:
            send_email_html(subject, html, to_override=row["email"])
            sent_count += 1
            print(f"  Sent to: {row['email']}")
        except Exception as e:
            print(f"  Failed to send to {row['email']}: {e}")
    
    # Also send to the main recipient
    try:
        send_email_html(subject, html)
        sent_count += 1
        print(f"  Sent to main recipient")
    except Exception as e:
        print(f"  Failed to send to main recipient: {e}")
    
    return sent_count
