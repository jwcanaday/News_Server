import os
import json
import logging
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator
import requests
import demjson3
from dateutil import parser as date_parser
import subprocess

# --- Configuration ---
BASE_JS_URL = "https://www.ag.state.mn.us/Office/Communications/_Scripts/pr{}.js"
BASE_LINK_URL = "https://www.ag.state.mn.us/Office/Communications/"
YEARS = range(2018, 2026)
CACHE_FILE = "seen_items.json"
RSS_FILE = "mn_ag_rss.xml"

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# --- Load Seen Links ---
seen = set()
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        try:
            seen = set(json.load(f))
        except Exception as e:
            logging.warning(f"Error loading cache: {e}")

# --- Clean JavaScript to JSON-Compatible String ---
def extract_and_clean_js(js_text):
    start = js_text.find("[")
    end = js_text.rfind("]") + 1
    raw = js_text[start:end]
    raw = re.sub(r"//.*?$", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)
    return raw

# --- Set up Feed Generator ---
fg = FeedGenerator()
fg.title("Minnesota AG Press Releases")
fg.link(href=BASE_LINK_URL, rel='alternate')
fg.link(href="https://jwcanaday.github.io/mn-ag-rss/mn_ag_rss.xml", rel='self')
fg.description("Latest press releases from the Minnesota Attorney General's Office")

new_links = set()
entry_count = 0

for year in YEARS:
    url = BASE_JS_URL.format(year)
    logging.info(f"Processing year {year} from {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        js = response.text

        js_clean = extract_and_clean_js(js)

        try:
            items = demjson3.decode(js_clean)
            logging.info(f"Parsed {len(items)} items for {year}")
        except Exception as e:
            logging.warning(f"demjson3 failed for {year}, trying partial parse: {e}")
            try:
                items = demjson3.decode_partial(js_clean)
                logging.info(f"Partially parsed {len(items)} items for {year}")
            except Exception as e2:
                logging.error(f"Failed even with decode_partial for {year}: {e2}")
                continue

        try:
            items.sort(key=lambda x: date_parser.parse(x["date"]), reverse=True)
        except Exception as e:
            logging.warning(f"Failed to sort items for {year}: {e}")

        for entry in items:
            try:
                link = BASE_LINK_URL + entry["file"]
                if link in seen:
                    continue

                title = entry["title"].strip()
                lede = entry.get("lede", "").strip() or "No description available."
                try:
                    pub_date = datetime.strptime(entry["date"], "%B %d, %Y").replace(tzinfo=timezone.utc)
                except ValueError:
                    pub_date = date_parser.parse(entry["date"]).replace(tzinfo=timezone.utc)

                fe = fg.add_entry()
                fe.title(title)
                fe.link(href=link)
                fe.guid(link, permalink=True)
                fe.pubDate(pub_date)
                fe.content(f"<p>{lede}</p><p><a href='{link}'>{link}</a></p>", type="CDATA")

                new_links.add(link)
                entry_count += 1
                logging.info(f"Added: {title}")

            except Exception as e:
                logging.warning(f"Error processing entry: {e}")

    except requests.HTTPError as e:
        logging.warning(f"Could not fetch {url}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error fetching {url}: {e}")

# --- Write RSS Feed ---
if entry_count > 0:
    fg.rss_file(RSS_FILE)
    logging.info(f"Wrote {entry_count} new entries to {RSS_FILE}")
else:
    logging.info("No new entries added.")

# --- Update Cache ---
if new_links:
    seen.update(new_links)
    with open(CACHE_FILE, "w") as f:
        json.dump(sorted(seen), f, indent=2)
    logging.info(f"Updated seen items cache with {len(new_links)} items.")

# --- Git Push (if changes made) ---
try:
    subprocess.run(["git", "add", RSS_FILE, CACHE_FILE], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-update RSS feed"], check=True)
    subprocess.run(["git", "push"], check=True)
    logging.info("RSS XML and cache pushed to GitHub.")
except subprocess.CalledProcessError as e:
    logging.warning(f"Git push failed or nothing to commit: {e}")
