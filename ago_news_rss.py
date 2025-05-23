import warnings
warnings.simplefilter("ignore")

import urllib3
from urllib3.exceptions import NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import re
import demjson3
import os
import logging
import json

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# --- Constants ---
BASE_URL = "https://www.ag.state.mn.us"
FEED_URL = f"{BASE_URL}/Office/Communications.asp"
YEARS = list(range(2018, 2026))
SEEN_ITEMS_FILE = "seen_items.json"

# --- Load cache ---
seen = set()
if os.path.exists(SEEN_ITEMS_FILE):
    with open(SEEN_ITEMS_FILE, "r") as f:
        seen = set(json.load(f))

# --- Prepare feed ---
fg = FeedGenerator()
fg.title("Minnesota AG Press Releases")
fg.link(href=FEED_URL, rel='alternate')
fg.link(href="https://jwcanaday.github.io/News_Server/mn_ag_rss.xml", rel='self')
fg.description("Latest press releases from the Minnesota Attorney General's Office")

new_items = []

# --- Process each year's JS file ---
for year in YEARS:
    js_url = f"{BASE_URL}/Office/Communications/_Scripts/pr{year}.js"
    logging.info(f"Processing year {year} from {js_url}")
    try:
        resp = requests.get(js_url)
        js_raw = resp.text.strip()

        js_clean = re.sub(r'^var pr\d+\s*=\s*', '', js_raw, count=1).strip().rstrip(';')
        entries = demjson3.decode(js_clean)

        logging.info(f"Parsed {len(entries)} items for {year}")
    except Exception as e:
        logging.error(f"Error parsing {js_url}: {e}")
        continue

    for entry in entries:
        try:
            # Normalize keys to lowercase
            entry = {k.lower(): v for k, v in entry.items()}

            date_str = entry.get("date", "").strip()
            if not date_str:
                logging.warning(f"Missing publication date. Entry keys: {list(entry.keys())}, Entry: {entry}")
                raise ValueError("Missing publication date")

            # Normalize date formatting
            normalized_date = date_str.strip()

            if re.match(r"^[A-Za-z]+ \d{1,2} \d{4}$", normalized_date):
                parts = normalized_date.split()
                normalized_date = f"{parts[0]} {parts[1]}, {parts[2]}"
            elif re.match(r"^[A-Za-z]+ \d{4}$", normalized_date):
                normalized_date = f"{normalized_date.split()[0]} 1, {normalized_date.split()[1]}"

            pub_date = datetime.strptime(normalized_date, "%B %d, %Y").replace(tzinfo=timezone.utc)

            title = entry.get("title", "").strip()
            link = entry.get("file", "").strip()
            lede = entry.get("lede", "").strip()

            full_url = link if link.startswith("http") else BASE_URL + "/Office/Communications/" + link

            if full_url in seen:
                continue

            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=full_url)
            fe.guid(full_url, permalink=True)
            fe.pubDate(pub_date)

            formatted_date = pub_date.strftime("%B %d, %Y")
            fe.content(
                f"<p><strong>Publication Date:</strong> {formatted_date}</p>"
                f"<p>{lede}</p>"
                f"<p><a href='{full_url}'>{full_url}</a></p>",
                type="CDATA"
            )

            new_items.append(full_url)
        except Exception as e:
            logging.warning(f"Error processing entry: {e}")

# --- Save updated feed and cache ---
if new_items:
    fg.rss_file("mn_ag_rss.xml")
    seen.update(new_items)
    with open(SEEN_ITEMS_FILE, "w") as f:
        json.dump(sorted(seen), f, indent=2)
    logging.info(f"Added {len(new_items)} new entries.")
else:
    logging.info("No new entries added.")
