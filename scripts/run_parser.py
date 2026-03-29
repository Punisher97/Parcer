import argparse
import asyncio
from pathlib import Path

from hhru_parser.db import SessionLocal
from hhru_parser.db.init_db import init_db
from hhru_parser.db.save_vacancy import save_vacancy
from hhru_parser.methods.http import HTTPParser
from hhru_parser.methods.http import create_async_client
from hhru_parser.methods.parse_vacancy import parse_vacancy_html
from hhru_parser.methods.search import collect_vacancies
from hhru_parser.stats.compute_by_vacancy import compute_average_salary
from hhru_parser.stats.compute_by_vacancy import get_salaries_by_query
from hhru_parser.stats.compute_by_vacancy import plot_salary_distribution


async def process_vacancy(
    parser: HTTPParser,
    item: dict,
    index: int,
    total: int,
    query: str,
    semaphore: asyncio.Semaphore,
) -> None:
    url = item["url"]

    async with semaphore:
        print(f"[{index}/{total}] Fetching {url}")
        try:
            html = await parser.fetch_text(url)
            data = parse_vacancy_html(html, url=url, query=query)

            if data["title"] is None:
                debug_dir = Path("debug")
                debug_dir.mkdir(parents=True, exist_ok=True)
                with open(debug_dir / "bad_vacancy.html", "w", encoding="utf-8") as file:
                    file.write(html)

            with SessionLocal() as session:
                saved = save_vacancy(session, data)

            print("Saved:", saved.title)

        except Exception as error:
            print("Error:", error)


async def async_main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("-n", type=int, default=20)
    parser.add_argument("--concurrency", type=int, default=10)

    args = parser.parse_args()

    query = args.query
    n = args.n
    concurrency = max(1, args.concurrency)

    print("Initializing DB...")
    init_db()

    async with await create_async_client() as client:
        http_parser = HTTPParser(client=client)

        print(f"Searching vacancies for: {query}")
        items = await collect_vacancies(http_parser, query, n)
        print(f"Found {len(items)} vacancies")

        semaphore = asyncio.Semaphore(concurrency)
        tasks = [
            process_vacancy(http_parser, item, i, len(items), query, semaphore)
            for i, item in enumerate(items, start=1)
        ]
        await asyncio.gather(*tasks)

    with SessionLocal() as session:
        avg_salary = compute_average_salary(session, query)
        print("Average salary:", avg_salary)

        salaries = get_salaries_by_query(session, query)
        plot_salary_distribution(salaries, query)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
