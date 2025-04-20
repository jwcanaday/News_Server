# download_js_ago.py
import os
import requests
from datetime import datetime

# Configuration
YEARS = list(range(2018, 2026))
BASE_URL = "https://www.ag.state.mn.us/Office/Communications/_Scripts/"
DEST_FOLDER = "historical_js_files"

# Create destination folder if not exists
os.makedirs(DEST_FOLDER, exist_ok=True)

def download_js(year):
    filename = f"pr{year}.js"
    url = f"{BASE_URL}{filename}"
    dest_path = os.path.join(DEST_FOLDER, filename)

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[✓] Downloaded {filename}")
    except Exception as e:
        print(f"[✗] Failed to download {filename}: {e}")

def main():
    print(f"Starting download of JS files at {datetime.now().isoformat()}")
    for year in YEARS:
        download_js(year)

if __name__ == "__main__":
    main()
