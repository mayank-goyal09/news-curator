# run_daily.py
# ═══════════════════════════════════════════════════════════════════
#  Complete Daily Pipeline:
#  1. Ingest RSS feeds (by category)
#  2. Curate with Ollama (21 news across 5 categories)
#  3. Generate TTS audio
#  4. Send email digest (to main + all subscribers)
# ═══════════════════════════════════════════════════════════════════

import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv()

from run_ingest import main as ingest_main
from run_curate import main as curate_main
from run_tts import main as tts_main
from run_send_email import main as email_main


def main():
    print("═" * 60)
    print("  EcoNews Daily Pipeline Started")
    print("═" * 60)

    print("\n▶ Step 1/4: Ingesting RSS feeds...")
    ingest_main()

    print("\n▶ Step 2/4: Curating with Ollama (21 news, 5 categories)...")
    curate_main()

    print("\n▶ Step 3/4: Generating TTS audio...")
    try:
        tts_main()
    except Exception as e:
        print(f"  ⚠ TTS failed (non-fatal): {e}")

    print("\n▶ Step 4/4: Sending email digest...")
    try:
        email_main()
    except Exception as e:
        print(f"  ⚠ Email failed (non-fatal): {e}")

    print("\n" + "═" * 60)
    print("  ✅ Daily Pipeline Complete!")
    print("═" * 60)


if __name__ == "__main__":
    main()
