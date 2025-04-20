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

Detailed informaiton about: 📄 historical_press_data_airtable_ready.csv
This CSV is the final cleaned and structured output file, optimized for import into Airtable. It was derived from the original historical_press_data.csv through a series of transformations to improve readability, stability, and usability.

✅ Enhancements applied:
Character Cleanup:
All text fields were normalized using Unicode standardization (NFKC) to remove encoding issues, smart quotes, and non-printable characters.

HTML Artifact Removal:
Any lingering HTML tags or markup were stripped from the full_text, summary, assets, and links fields using BeautifulSoup.

Whitespace and Line Break Normalization:
Extra line breaks and excessive spacing were collapsed into single spaces. This improves compatibility with spreadsheet views and prevents overflow in Airtable cells.

Column Splitting and Flattening:

The original assets and links fields (which were comma- or semicolon-separated lists) were split into structured arrays.

These arrays were flattened into newline-separated strings to improve Airtable rendering and filtering.

Each entry appears on its own line inside the cell in Airtable.

Link entries also include labels and file type categories (pdf, html, doc, other).

Field Renaming for Record Matching:

The url column was renamed to record_url to serve as a unique identifier during Airtable import.

This enables “Update existing records” logic by matching each row to a corresponding Airtable record using the record_url.

Preserved Metadata:

last_scraped: UTC timestamp of when the script last retrieved each press release

asset_count: Count of unique assets extracted per release

🔁 Intended Usage:
This file is ready for bulk import into Airtable using the “Update by matching” feature. It assumes that the original Airtable base contains a record_url field corresponding to each press release's URL.



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
