from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from hhru_parser.methods.http import HTTPParser

BASE_SEARCH_URL = "https://hh.ru/search/vacancy"


def parse_search_page(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    cards = soup.find_all("div", id=True)

    for card in cards:
        classes = card.get("class", [])
        if not any("vacancy-card" in el for el in classes):
            continue

        vacancy_id = card.get("id")
        if not vacancy_id or not vacancy_id.isdigit():
            continue

        title_el = card.find(attrs={"data-qa": "serp-item__title-text"})
        company_el = card.find(attrs={"data-qa": "vacancy-serp__vacancy-employer-text"})
        address_el = card.find(attrs={"data-qa": "vacancy-serp__vacancy-address"})

        title = title_el.get_text(" ", strip=True) if title_el else None
        company = company_el.get_text(" ", strip=True) if company_el else None
        address = address_el.get_text(" ", strip=True) if address_el else None

        results.append({
            "vacancy_id": int(vacancy_id),
            "title": title,
            "url": f"https://hh.ru/vacancy/{vacancy_id}",
            "company": company,
            "address": address,
        })

    return results


async def collect_vacancies(parser, query, number_of_vacancies):
    page = 0
    items = []
    seen_ids = set()

    while len(items) < number_of_vacancies:
        search_url = (
            f"{BASE_SEARCH_URL}?text={quote_plus(query)}&page={page}"
        )

        html = await parser.fetch_text(search_url)
        page_items = parse_search_page(html)

        if not page_items:
            break

        added = 0
        for item in page_items:
            vid = item["vacancy_id"]

            if vid in seen_ids:
                continue

            seen_ids.add(vid)
            items.append(item)
            added += 1

            if len(items) >= number_of_vacancies:
                break

        if added == 0:
            break

        page += 1

    return items[:number_of_vacancies]
