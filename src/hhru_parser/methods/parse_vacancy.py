from bs4 import BeautifulSoup
import re


def extract_vacancy_id(url):
    parts = url.rstrip("/").split("/")
    if parts and parts[-1].isdigit():
        return int(parts[-1])
    return None


def parse_salary_avg(salary_text):
    DOLLAR_RATE = 80
    USD_THRESHOLD = 20000

    if not salary_text:
        return None

    salary_text = salary_text.replace("\xa0", " ")

    numbers = re.findall(r"\d[\d ]*", salary_text)
    values = []

    for num in numbers:
        num = num.replace(" ", "")
        if num.isdigit():
            num_int = int(num)

            if num_int < USD_THRESHOLD:
                num_int *= DOLLAR_RATE

            values.append(num_int)

    if not values:
        return None

    if len(values) == 1:
        return values[0]

    return (values[0] + values[1]) // 2


def parse_vacancy_html(html, url, query=None):
    soup = BeautifulSoup(html, "html.parser")

    title_el = soup.find(attrs={"data-qa": "vacancy-title"})
    title = title_el.get_text(" ", strip=True) if title_el else None

    experience_el = soup.find(attrs={"data-qa": "vacancy-experience"})
    experience = experience_el.get_text(" ", strip=True) if experience_el else None

    company_el = soup.find(attrs={"data-qa": "vacancy-company-name"})
    company = company_el.get_text(" ", strip=True) if company_el else None

    salary = None
    if title_el and title_el.parent:
        salary_span = title_el.parent.find("span")
        if salary_span:
            salary = salary_span.get_text(" ", strip=True)

    desc_el = soup.find("div", class_="vacancy-description")
    description = desc_el.get_text(" ", strip=True) if desc_el else ""

    salary_avg = parse_salary_avg(salary)
    vacancy_id = extract_vacancy_id(url)

    return {
        "vacancy_id": vacancy_id,
        "url": url,
        "title": title,
        "company": company,
        "experience": experience,
        "salary_text": salary,
        "salary_avg": salary_avg,
        "description": description,
        "query": query,
    }
