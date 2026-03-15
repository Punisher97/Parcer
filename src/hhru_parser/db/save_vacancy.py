from sqlalchemy import select
from sqlalchemy.orm import Session

from hhru_parser.db.models import Vacancy

def save_vacancy(session: Session, data: dict) -> Vacancy:
    vacancy = None

    vacancy_id = data.get("vacancy_id")
    url = data.get("url")

    if vacancy_id is not None:
        vacancy = session.scalar(
            select(Vacancy).where(Vacancy.vacancy_id == vacancy_id)
        )

    if vacancy is None and url is not None:
        vacancy = session.scalar(
            select(Vacancy).where(Vacancy.url == url)
        )

    if vacancy is None:
        vacancy = Vacancy(url=url)
        session.add(vacancy)

    vacancy.vacancy_id = data.get("vacancy_id")
    vacancy.title = data.get("title")
    vacancy.company = data.get("company")
    vacancy.salary_text = data.get("salary_text")
    vacancy.salary_avg = data.get("salary_avg")
    vacancy.experience = data.get("experience")
    vacancy.description = data.get("description")

    session.commit()
    session.refresh(vacancy)
    return vacancy