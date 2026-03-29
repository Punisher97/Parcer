from __future__ import annotations

from typing import Iterable
from typing import Optional

import matplotlib.pyplot as plt
from sqlalchemy.orm import Session

from hhru_parser.db.models import Vacancy


def compute_average_salary(session: Session, query: Optional[str] = None) -> Optional[float]:
    q = session.query(Vacancy).filter(Vacancy.salary_avg.is_not(None))
    if query:
        q = q.filter(Vacancy.query == query)

    salaries = [item.salary_avg for item in q.all() if item.salary_avg is not None]
    if not salaries:
        return None

    return round(sum(salaries) / len(salaries), 2)


def get_salaries_by_query(session: Session, query: Optional[str] = None) -> list[int]:
    q = session.query(Vacancy).filter(Vacancy.salary_avg.is_not(None))
    if query:
        q = q.filter(Vacancy.query == query)

    return [item.salary_avg for item in q.all() if item.salary_avg is not None]


def plot_salary_distribution(salaries: Iterable[int], query: str) -> None:
    salaries = list(salaries)
    if not salaries:
        print("No salary data to plot")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(salaries, bins=20)
    plt.title(f"Salary distribution for query: {query}")
    plt.xlabel("Salary")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("salary_plot.png")
    plt.close()
