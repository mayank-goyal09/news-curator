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


def send_email_html(subject: str, html: str) -> None:
    sender = _get_env("NEWS_EMAIL_SENDER")
    to_addr = _get_env("NEWS_EMAIL_TO")

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
        # Optional debug: set NEWS_EMAIL_DEBUG=1 in .env if needed
        if os.getenv("NEWS_EMAIL_DEBUG") == "1":
            smtp.set_debuglevel(1)  # prints SMTP conversation [web:478]

        smtp.login(sender, app_password)
        smtp.send_message(msg)
