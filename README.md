# Minnesota AG Press Releases RSS Feed

[![RSS Build Status](https://github.com/jwcanaday/mn-ag-rss/actions/workflows/generate_rss.yml/badge.svg)](https://github.com/jwcanaday/mn-ag-rss/actions/workflows/generate_rss.yml)
[![Last Commit](https://img.shields.io/github/last-commit/jwcanaday/mn-ag-rss)](https://github.com/jwcanaday/mn-ag-rss)
[![RSS Feed Valid](https://img.shields.io/badge/feed-valid-brightgreen)](https://validator.w3.org/feed/check.cgi?url=https%3A%2F%2Fjwcanaday.github.io%2Fmn-ag-rss%2Fmn_ag_rss.xml)

This project generates and publishes a live RSS feed from the Minnesota Attorney General's Office website, which does not natively provide one. The feed is built using a custom Python script and updated twice daily via GitHub Actions. The system integrates with Feedly, Zapier, and Airtable to provide a fully automated alerting and archival workflow.

---

## 🔧 What the Script Does

The Python script (`ago_news_rss.py`) automates:

1. **Scraping JavaScript data** files (`prYYYY.js`) from the MN AG site.
2. **Parsing** those non-standard JavaScript arrays using `demjson3`.
3. **Sorting releases** from newest to oldest.
4. **Skipping duplicates** using a `seen_items.json` cache.
5. **Generating an RSS 2.0 XML feed** using `feedgen`.
6. **Committing and pushing updates** to the GitHub repo automatically.
7. **Logging errors and status** via GitHub Actions.

---

## 📡 RSS Feed Hosting via GitHub Pages

The output RSS feed is hosted via GitHub Pages at:

**RSS Feed URL**:  
```
https://jwcanaday.github.io/mn-ag-rss/mn_ag_rss.xml
```

A `.nojekyll` file ensures that GitHub Pages serves the XML file correctly.

---

## 🔁 GitHub Actions Automation

The workflow (`.github/workflows/generate_rss.yml`) is scheduled to run **twice daily**:

- ⏰ 12:00 PM Central (17:00 UTC)
- ⏰ 6:00 PM Central (23:00 UTC)

It performs the following steps:

- Checks out the latest code
- Installs Python dependencies
- Runs `ago_news_rss.py`
- Commits any changes to `mn_ag_rss.xml` and `seen_items.json`
- Pushes to the `main` branch
- **Automatically creates an issue** if the script fails

---

## 🔄 Workflow Integration

This system is fully integrated with cloud tools:

### 📰 Feedly
Feedly subscribes to the live GitHub-hosted RSS feed.

### 🤖 Zapier
Zapier automation adds each new Feedly item to an Airtable base.

### 📬 Airtable
Airtable automation emails the user whenever a new record is added.

---

## 🗂 Project Structure

```
.
├── ago_news_rss.py          # Main script: scrapes, builds RSS, pushes to GitHub
├── mn_ag_rss.xml            # Live RSS feed file (auto-updated)
├── seen_items.json          # Cache of seen entries to prevent duplicates
├── .github/
│   └── workflows/
│       └── generate_rss.yml # GitHub Actions: scheduled twice daily
├── .nojekyll                # Ensures raw XML served correctly by GitHub Pages
└── README.md                # This documentation
```

---

## 🛠 Requirements

If running locally:

```bash
pip install feedgen demjson3 python-dateutil
```

You’ll also need Git configured to commit and push to your GitHub repo.

---

## 🚀 Future Enhancements

- Add keyword filtering or tag-based alerts
- Extract full HTML or documents from press releases
- Archive PDFs or generate summaries for Airtable
- Sync Airtable to backup storage or databases

---

## 👤 Maintainer

This project is maintained by [@jwcanaday](https://github.com/jwcanaday) for monitoring and analysis of public press releases from the MN AG's Office.
