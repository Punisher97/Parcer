from pathlib import Path

from hhru_parser.methods.parse_vacancy import parse_vacancy_html

from hhru_parser.db.init_db import init_db
from hhru_parser.db import SessionLocal
from hhru_parser.db.save_vacancy import save_vacancy


def main():
    init_db()
    html = Path("debug/vacancy_2.html").read_text(encoding="utf-8")

    data = parse_vacancy_html(
        html,
        url="https://hh.ru/vacancy/123456"
    )

    print("PARSED DATA:")
    print(data)

    with SessionLocal() as session:
        vacancy = save_vacancy(session, data)

    print("\nSaved vacancy with DB id:", vacancy.id)


if __name__ == "__main__":
    main()