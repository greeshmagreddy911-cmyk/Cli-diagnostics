import csv
import time
from collections import Counter

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


URL = "https://books.toscrape.com/"
OUTPUT_FILE = "output.csv"


def create_session():
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Task4-WebScraper/1.0"
        }
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def scrape_books(url):
    session = create_session()

    response = session.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for item in soup.select("article.product_pod"):
        title_tag = item.select_one("h3 a")
        price_tag = item.select_one(".price_color")
        rating_tag = item.select_one("p.star-rating")

        books.append(
            {
                "title": title_tag.get("title", "").strip(),
                "price": price_tag.get_text(strip=True),
                "rating": (
                    rating_tag.get("class", ["", "Unknown"])[1]
                    if rating_tag
                    else "Unknown"
                ),
            }
        )

        time.sleep(0.2)

    return books


def save_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["title", "price", "rating"],
        )
        writer.writeheader()
        writer.writerows(data)


def generate_summary(data):
    ratings = Counter(item["rating"] for item in data)

    return {
        "total_books": len(data),
        "rating_distribution": dict(ratings),
    }


def main():
    books = scrape_books(URL)
    save_csv(books, OUTPUT_FILE)

    summary = generate_summary(books)

    print("Scraping completed successfully.")
    print(f"Records extracted: {summary['total_books']}")
    print(f"Rating distribution: {summary['rating_distribution']}")
    print(f"CSV output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
