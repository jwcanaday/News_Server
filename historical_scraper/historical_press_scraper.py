# historical_press_scraper.py
import os
import csv
import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime

# --- Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "html_cache")
OUTPUT_FILE = os.path.join(BASE_DIR, "historical_press_data.csv")
INPUT_FILE = os.path.join(BASE_DIR, "mn_ag_press_releases.csv")  # CSV from your existing Airtable export

os.makedirs(CACHE_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# --- Helpers ---
def fetch_and_cache_html(url):
    parsed = urlparse(url)
    cache_filename = os.path.join(CACHE_DIR, parsed.path.replace('/', '_'))
    if os.path.exists(cache_filename):
        logging.info(f"Using cached HTML for: {url}")
        with open(cache_filename, "r", encoding="utf-8") as f:
            return f.read(), True

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        with open(cache_filename, "w", encoding="utf-8") as f:
            f.write(resp.text)
        logging.info(f"Fetched and cached HTML for: {url}")
        return resp.text, False
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None, False

def extract_content_and_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", id="content")
    if not content_div:
        return "", [], []

    full_text = content_div.get_text(separator="\n", strip=True)

    links = []
    assets = set()

    for a in content_div.find_all("a", href=True):
        href = urljoin(base_url, a['href'])
        text = a.get_text(strip=True) or os.path.basename(href)
        ext = os.path.splitext(href)[-1].lower()
        category = "other"
        if ext in [".pdf"]:
            category = "pdf"
        elif ext in [".doc", ".docx"]:
            category = "doc"
        elif ext in [".htm", ".html"]:
            category = "html"
        
        if href not in assets:
            links.append({
                "url": href,
                "label": text,
                "type": category
            })
            assets.add(href)

    return full_text, links, sorted(assets)

def generate_summary(text, max_chars=300):
    return text[:max_chars].replace("\n", " ") + "..." if len(text) > max_chars else text

# --- Main ---
def run():
    with open(INPUT_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        entries = list(reader)

    output_fields = ["url", "last_scraped", "full_text", "summary", "asset_count", "assets", "links"]
    rows = []

    for entry in entries:
        url = entry.get("url")
        if not url:
            continue

        html, from_cache = fetch_and_cache_html(url)
        if not html:
            continue

        full_text, links, assets = extract_content_and_links(html, base_url=url)
        summary = generate_summary(full_text)
        
        row = {
            "url": url,
            "last_scraped": datetime.utcnow().isoformat(),
            "full_text": full_text,
            "summary": summary,
            "asset_count": len(assets),
            "assets": ", ".join(assets),
            "links": "; ".join([f"{l['label']} ({l['type']}) - {l['url']}" for l in links])
        }

        rows.append(row)
        time.sleep(0.5)  # polite delay

    with open(OUTPUT_FILE, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)

    logging.info(f"Data written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    run()

