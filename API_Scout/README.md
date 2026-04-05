# 📡 API Scout (CoinGecko Proof-of-Concept)

A lightweight, synchronous Python utility designed to scout, test, and validate endpoints from the external **CoinGecko API**. 

This module serves as a **Proof of Concept (PoC)** for external API interaction. It was used to understand the data structures and rate limits of the CoinGecko API before implementing the asynchronous version in the main Telegram Bot.

## ✨ Features
- Fetches real-time lists of supported cryptocurrencies and fiat currencies.
- Demonstrates randomized API querying using Python's `random.choice`.
- Includes basic `try/except` graceful degradation for network failures (`requests.exceptions.RequestException`).

## 🛠 Tech Stack
- `Python 3.x`
- `requests` (Synchronous HTTP client)

## 🚀 Quick Start

1. Ensure you have the required library installed:
   ```bash
   pip install requests
   ```
2. Run the script:
   ```
   python main.py
   ```
3. **Expected Output**: The script will output the current prices of 3 random cryptocurrencies against random fiat currencies, with a 1-second delay between requests to respect API rate limits.