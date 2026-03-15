from sqlalchemy import select
from hhru_parser.db.models import Vacancy
import matplotlib.pyplot as plt


def get_salaries_by_query(session, query: str) -> list[int]:
    vacancies = session.scalars(select(Vacancy)).all()

    query_lower = query.lower()
    salaries = []

    for vacancy in vacancies:
        title = vacancy.title or ""
        description = vacancy.description or ""

        text = f"{title} {description}".lower()

        if query_lower in text and vacancy.salary_avg is not None:
            salaries.append(vacancy.salary_avg)

    return salaries


def compute_average_salary(session, query: str) -> float | None:
    salaries = get_salaries_by_query(session, query)

    if not salaries:
        return None

    return round(sum(salaries) / len(salaries))


def plot_salary_distribution(salaries: list[int], query: str) -> None:
    if not salaries:
        print("No salaries to plot")
        return

    plt.figure(figsize=(10, 6))
    plt.hist(salaries, bins=60)
    plt.xlabel("Salary")
    plt.ylabel("Count")
    plt.title(f"Salary distribution for {query}")
    plt.grid(True)
    plt.savefig("salary_plot.png")
    print("Plot saved to salary_plot.png")



