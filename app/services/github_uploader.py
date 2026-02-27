import os
import subprocess
from pathlib import Path

def get_env_or_raise(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise ValueError(f"Missing environment variable: {key}")
    return val

def upload_audio_to_github(audio_path: str) -> str:
    """
    Commits and pushes the audio file to the configured GitHub repository.
    Returns the public URL (raw or GitHub Pages) for the audio.
    """
    # E.g. "mayank-goyal09/news-curator"
    github_repo = os.getenv("GITHUB_REPO", "")
    # E.g. "https://mayank-goyal09.github.io/news-curator"
    github_pages_base = os.getenv("GITHUB_PAGES_BASE_URL", "")

    if not github_repo:
        print("Warning: GITHUB_REPO not set in .env. Skipping GitHub upload.")
        return ""

    try:
        audio_path_obj = Path(audio_path)
        # Ensure it's tracked by git
        subprocess.run(["git", "add", str(audio_path_obj)], check=True, capture_output=True)
        
        # Commit it
        commit_msg = f"Update daily audio digest: {audio_path_obj.name}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
        
        print(f"Git: Committed {audio_path_obj.name}")
        
        # Push it
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        print("Git: Pushed to origin/main successfully.")

        # Construct public URL
        # If GitHub Pages is configured, use it, else fallback to raw githubusercontent
        if github_pages_base:
            # e.g., https://mayank-goyal09.github.io/news-curator/data/audio/digest_YYYY-MM-DD.mp3
            base = github_pages_base.rstrip("/")
            # Normalize path to use forward slashes for the web URL
            web_path = str(audio_path_obj).replace("\\", "/")
            public_url = f"{base}/{web_path}"
        else:
            # Fallback to direct raw download URL (handles audio MIME types correctly)
            web_path = str(audio_path_obj).replace("\\", "/")
            public_url = f"https://github.com/{github_repo}/raw/main/{web_path}"

        print(f"Public Audio URL: {public_url}")
        return public_url

    except subprocess.CalledProcessError as e:
        print(f"Failed to upload to GitHub: {e.stderr.decode('utf-8') if e.stderr else str(e)}")
        print("Make sure your project is a git repository and 'origin' is set.")
        return ""
