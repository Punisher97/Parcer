from bs4 import BeautifulSoup

def parse_vacancy_html(html: str) -> dict:
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

    return {
        "title": title,
        "company": company,
        "experience": experience,
        "salary_text": salary,
        "description": description,
    }