from bs4 import BeautifulSoup
import re

def extract_vacancy_id(url: str) -> int | None:
    parts = url.rstrip("/").split("/")
    if parts and parts[-1].isdigit():
        return int(parts[-1])
    return None


def parse_salary_avg(salary_text: str | None) -> int | None:
    if not salary_text:
        return None

    salary_text = salary_text.replace("\xa0", " ")

    numbers = re.findall(r"\d[\d ]*", salary_text)
    values = []

    for num in numbers:
        num = num.replace(" ", "")
        if num.isdigit():
            values.append(int(num))

    if not values:
        return None

    if len(values) == 1:
        return values[0]

    return sum(values[:2]) // 2

    
        
        

def parse_vacancy_html(html: str, url: str) -> dict:
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
    description = desc_el.get_text(" ", strip=True) if desc_el else None

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
    }