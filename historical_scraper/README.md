# Historical Press Release Scraper

This folder contains a standalone script and supporting files used to backfill press release content from the Minnesota Attorney General's website.

It scrapes the full text and linked documents for press releases already captured in the RSS feed and Airtable, and outputs a structured CSV suitable for updating those records.

---

## 📁 Contents

- **`historical_press_scraper.py`**  
  The main Python script that performs the following:
  - Loads a CSV of press release URLs (from your Airtable export)
  - Fetches and caches each page's HTML
  - Extracts the full press release text from `<div id="content">`
  - Parses all document links (PDFs, DOCs, etc.) and classifies them
  - Generates a short summary for each press release
  - Detects duplicates and logs scraping metadata (e.g., `last_scraped` date)
  - Outputs clean CSVs for import into Airtable

- **`mn_ag_press_releases.csv`**  
  The input file with a list of press release URLs and basic metadata from Airtable.

- **`historical_press_data_cleaned.csv`**  
  An intermediate file containing cleaned full text and assets.

- **`historical_press_data_airtable_ready.csv`**  
  Final CSV ready for import into Airtable. Includes:
  - `record_url` (for matching)
  - `summary`, `full_text`
  - `asset_list` and `link_list` (newline-separated for easy display)

- **`html_cache/`**  
  A local cache of each downloaded HTML page, used to avoid redundant requests and speed up future runs.

---

## 🧰 Requirements

Run this script using Python 3. Recommended modules:

```bash
pip install requests beautifulsoup4 lxml
```

---

## 🚀 Usage

```bash
python3 historical_press_scraper.py
```

The script will:
- Cache or reuse existing HTML for each press release
- Output results to a structured CSV for Airtable import

---

## 🧠 Notes

- The script includes retry and normalization logic for malformed or incomplete entries.
- Use `record_url` as the unique identifier when importing into Airtable to update existing records.

---

## 📌 Future Considerations

This scraper was designed for one-time historical enrichment. The ongoing RSS automation handles new press releases.

If you wish to add full-text scraping to the RSS feed pipeline in the future, this logic can be modularly adapted.
