from typing import Any

from sqlalchemy.orm import Session

from hhru_parser.db.cache import vacancy_exists
from hhru_parser.db.models import Vacancy


ALLOWED_FIELDS = {
    "vacancy_id",
    "url",
    "query",
    "title",
    "company",
    "salary_text",
    "salary_avg",
    "description",
}


def save_vacancy(session: Session, data: dict[str, Any]) -> Vacancy:
    vacancy_id = str(data["vacancy_id"])
    url = str(data["url"])

    existing = session.query(Vacancy).filter(Vacancy.vacancy_id == vacancy_id).first()
    if existing is None:
        existing = session.query(Vacancy).filter(Vacancy.url == url).first()

    payload = {key: value for key, value in data.items() if key in ALLOWED_FIELDS}

    if existing is not None:
        for key, value in payload.items():
            setattr(existing, key, value)
        session.commit()
        session.refresh(existing)
        return existing

    if vacancy_exists(session, vacancy_id, url):
        existing = session.query(Vacancy).filter(Vacancy.vacancy_id == vacancy_id).first()
        if existing is None:
            existing = session.query(Vacancy).filter(Vacancy.url == url).first()
        if existing is not None:
            return existing

    vacancy = Vacancy(**payload)
    session.add(vacancy)
    session.commit()
    session.refresh(vacancy)
    return vacancy
