from hhru_parser.db import SessionLocal
from hhru_parser.db.models import Vacancy


def main() -> None:
    with SessionLocal() as session:
        deleted = session.query(Vacancy).delete()
        session.commit()
        print(f"Deleted {deleted} records")


if __name__ == "__main__":
    main()
