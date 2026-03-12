import argparse

from hhru_parser.methods.search import collect_vacancy_urls
from hhru_parser.methods.http import fetch_text
from hhru_parser.methods.parse_vacancy import parse_vacancy_html

from hhru_parser.db.init_db import init_db
from hhru_parser.db import SessionLocal
from hhru_parser.db.save_vacancy import save_vacancy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("-n", type=int, default=20)

    args = parser.parse_args()

    query = args.query
    n = args.n

    print("Initializing DB...")
    init_db()

    print(f"Searching vacancies for: {query}")

    items = collect_vacancy_urls(query, n)

    print(f"Found {len(items)} vacancies")

    with SessionLocal() as session:

        for i, item in enumerate(items, start=1):

            url = item["url"]

            print(f"[{i}/{len(items)}] Fetching {url}")

            try:
                html = fetch_text(url)

                data = parse_vacancy_html(html, url=url)

                save_vacancy(session, data)

                print("Saved:", data["title"])

            except Exception as e:
                print("Error:", e)


if __name__ == "__main__":
    main()