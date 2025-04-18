# Minnesota AG Press Releases RSS Feed

[![Last Commit](https://img.shields.io/github/last-commit/jwcanaday/mn-ag-rss)](https://github.com/jwcanaday/mn-ag-rss)
[![RSS Feed Valid](https://img.shields.io/badge/feed-valid-brightgreen)](https://validator.w3.org/feed/check.cgi?url=https%3A%2F%2Fjwcanaday.github.io%2Fmn-ag-rss%2Fmn_ag_rss.xml)

This project creates a live RSS feed from the Minnesota Attorney General's Office website, which does not natively provide one. It enables real-time monitoring and automation of press release activity using Python, GitHub Pages, Feedly, Zapier, and Airtable.

---

## 🔧 What the Script Does

The included Python script (`ago_news_rss.py`) automates the process of:

1. **Retrieving press release metadata** from JavaScript files (`prYYYY.js`) hosted by the MN AG's Office.
2. **Parsing** the non-standard JavaScript into structured data using `demjson3`.
3. **Sorting entries** by publication date (newest first).
4. **Skipping duplicates** using a `seen_items.json` cache file.
5. **Generating a valid RSS 2.0 feed** using `feedgen`, and outputting to `mn_ag_rss.xml`.
6. **Logging progress and issues** to assist with troubleshooting.

> Note: The script **does not extract full HTML content** or documents (e.g., PDFs) from the press release URLs.

---

## 📡 Live Feed Hosting via GitHub Pages

The `mn_ag_rss.xml` file is hosted via GitHub Pages, making it accessible as a public RSS feed:

**Feed URL**:  
```
https://jwcanaday.github.io/mn-ag-rss/mn_ag_rss.xml
```

A `.nojekyll` file is included to ensure the XML file is served with the correct content type (`application/xml`).

---

## 🔄 Workflow Integration

This feed powers a fully automated workflow:

### 1. 📰 Feedly Subscription
Feedly subscribes to the GitHub-hosted RSS feed. New entries appear as updates in Feedly.

### 2. 🤖 Zapier Automation
Zapier is configured to trigger when a new item appears in the Feedly feed:
- **Action**: Add a new record to an Airtable base

### 3. 📬 Airtable Notification
Airtable automation is set up to:
- Send an **email notification** to the user each time a new record is added to the table

---

## 🗂 Folder Structure

```
.
├── ago_news_rss.py          # Main script to generate the RSS feed
├── mn_ag_rss.xml            # Output RSS feed (served via GitHub Pages)
├── seen_items.json          # Local cache of previously seen entries
├── .nojekyll                # Prevents Jekyll processing on GitHub Pages
└── README.md                # This file
```

---

## 🛠 Requirements

Install dependencies with:

```bash
pip install feedgen demjson3 python-dateutil
```

---

## 🚀 Future Improvements (Optional)

- Push script-generated RSS to GitHub automatically
- Extract and archive PDF or document links from press releases
- Add filters for keyword-based routing (e.g., "opioid", "antitrust")
- Full-text scraping of press release content

---

## 👤 Maintainer

This project was developed and is maintained by [@jwcanaday](https://github.com/jwcanaday) for personal use, monitoring, and analysis of public press activity.
