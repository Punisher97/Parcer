from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from hhru_parser.db import Base

class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    vacancy_id: Mapped[int] = mapped_column(Integer, unique=True)

    url: Mapped[str] = mapped_column(String)

    title: Mapped[str | None] = mapped_column(String)

    company: Mapped[str | None] = mapped_column(String)

    salary_text: Mapped[str | None] = mapped_column(String)

    description: Mapped[str | None] = mapped_column(Text)