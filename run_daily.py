# run_daily.py
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
load_dotenv()

from run_ingest import main as ingest_main
from run_curate import main as curate_main
from run_send_email import main as email_main


def main():
    print("Daily job started")
    ingest_main()
    curate_main()
    email_main()
    print("Daily job finished successfully")


if __name__ == "__main__":
    main()
