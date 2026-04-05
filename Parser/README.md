# 🕷️ Hacker News Data Extractor (Parser)

A structured web scraping module designed to extract news articles, scores, and metadata from **Hacker News (YCombinator)**.

This tool parses raw HTML DOM into structured data and exports it for future database ingestion or AI processing.

## ✨ Features

- **Pagination Handling:** Automatically iterates through multiple pages (currently set to 5) to gather a larger dataset.
- **DOM Parsing:** Extracts specific elements (Titles, Links, Scores, Age) using CSS selectors via `BeautifulSoup4`.
- **Link Normalization:** Automatically converts relative item links into absolute URLs.
- **CSV Export:** Uses `csv.DictWriter` to safely export the parsed dictionaries into a structured `hacker_news.csv` file.
- **Error Handling:** Catches HTTP errors (`raise_for_status`) and connection drops to prevent crashes during the scraping process.

## 🛠 Tech Stack

- `Python 3.x`
- `requests` (HTML fetching)
- `BeautifulSoup4` (HTML parsing)
- `csv` (Built-in data export)

## 🚀 Quick Start

1. Install the required dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```
2. Run the scraper:
   ```
   python parser.py
   ```
3. **Expected Result**: The console will display the parsing status, and a hacker_news.csv file containing the structured data will be generated in the root directory.
