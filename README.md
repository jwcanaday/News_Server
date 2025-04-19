# Minnesota AG Press Release RSS Generator

This repository contains a Python script and GitHub Actions workflow to automatically generate an RSS feed from press release data published by the Minnesota Attorney General's Office. The AG’s website does not provide an RSS feed, so this system scrapes historical JavaScript-based content and transforms it into a standards-compliant RSS XML feed.

---

## 📌 Features

- ✅ Scrapes historical press releases from JS files for years 2018–2025
- ✅ Handles multiple variations in date formatting
- ✅ Filters out duplicates based on a local cache (`seen_items.json`)
- ✅ Outputs a clean `mn_ag_rss.xml` RSS feed suitable for Feedly, Zapier, and other readers
- ✅ Runs automatically twice daily (12pm and 6pm Central Time)
- ✅ Publishes updated RSS feed to GitHub Pages
- ✅ Logs issues and creates GitHub issues on failure (via PAT)

---

## 📂 Output Files

- `mn_ag_rss.xml` – The current RSS feed (viewable at https://jwcanaday.github.io/News_Server/mn_ag_rss.xml)
- `seen_items.json` – Cache of processed press release URLs to avoid duplicates

---

## ⚙️ GitHub Actions Automation

The script is run by a scheduled GitHub Actions workflow defined in `.github/workflows/generate_rss.yml`. Key functionality includes:

- Setting up Python and dependencies
- Running `ago_news_rss.py`
- Committing and pushing updates to `mn_ag_rss.xml` and `seen_items.json`
- Automatically creating an issue if the script fails (using `PAT_FOR_ISSUES` secret)

---

## 🛠️ Key Script Enhancements

- **Robust date normalization**: Handles irregular formats such as:
  - `"January 19 2022"` → `"January 19, 2022"`
  - `"December 2018"` → `"December 1, 2018"`
- **Key normalization**: Accepts both `Date` and `date`, `Title` and `title`, etc.
- **Inline publication date**: Includes `<pubDate>` and visible publication date in `<content>` for use in Zapier and Feedly automations

---

## 🔁 Integration with Feedly + Zapier + Airtable

1. **Feedly** subscribes to the GitHub-hosted RSS feed.
2. **Zapier** watches the Feedly RSS feed for new items.
3. **Zapier automation** pushes each new item into Airtable.
4. **Airtable automation** emails the user whenever a new record is created.

This setup ensures real-time delivery and tracking of press releases in your preferred workspace.

---

## 🧩 Future Enhancements (Under Consideration)

- Full HTML scraping of press release content (`<div id="content">`)
- Preservation of PDF and document hyperlinks
- Categorization and tagging of press releases by subject
- Airtable backfill and syncing from RSS

---

## 📄 License

MIT License. This repository is maintained for personal workflow automation and may be extended or forked under open terms.

---

## 🙋‍♂️ Maintainer

Created and maintained by [@jwcanaday](https://github.com/jwcanaday)
