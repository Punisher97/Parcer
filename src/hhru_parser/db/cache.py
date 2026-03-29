from sqlalchemy.orm import Session

from hhru_parser.db.models import Vacancy


def vacancy_exists(session: Session, vacancy_id: str, url: str) -> bool:
    by_id = session.query(Vacancy).filter(Vacancy.vacancy_id == vacancy_id).first()
    if by_id is not None:
        return True

    by_url = session.query(Vacancy).filter(Vacancy.url == url).first()
    return by_url is not None
