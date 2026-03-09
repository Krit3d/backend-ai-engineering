from bs4 import BeautifulSoup
import requests
import csv

BASE_URL = "https://news.ycombinator.com/"
CSV_FILENAME = "hacker_news.csv"


def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    except requests.exceptions.HTTPError as http_err:
        print(f"Server Error: {type(http_err).__name__}")
        return None

    except requests.exceptions.RequestException as req_err:
        print(f"Your request returned an exception: {type(req_err).__name__}.")
        return None


def parse_news(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    news_data = []

    items = soup.find_all("tr", class_="athing submission")

    for item in items:
        title_tag = item.select_one(".titleline > a")
        title = title_tag.text if title_tag else "No title"
        link = title_tag.get("href") if title_tag else ""

        if link.startswith("item"):
            link = BASE_URL + link

        subtext_row = item.find_next_sibling("tr")

        score_tag = subtext_row.select_one(".score")
        score = score_tag.text if score_tag else "0 points"

        age_tag = subtext_row.select_one(".age")
        age = age_tag.text if age_tag else "N/A"

        news_data.append(
            {"Title": title, "Link": link, "Score": score, "Age": age}
        )

    return news_data


def save_to_csv(data, filename):
    if not data:
        print("No data to save")
        return

    headers = data[0].keys()

    with open(filename, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"Successfully saved {len(data)} news in {filename}")


def main():
    print("Parsing...")
    html = fetch_html(BASE_URL)

    if html is not None:
        parsed_data = parse_news(html)
        save_to_csv(parsed_data, CSV_FILENAME)
    else:
        print("Parsing canceled due to an Error")


if __name__ == "__main__":
    main()
