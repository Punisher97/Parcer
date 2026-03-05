from pathlib import Path
from hhru_parser.methods.parse_vacancy import parse_vacancy_html

def main():
    html = Path("debug/vacancy.html").read_text(encoding="utf-8")
    data = parse_vacancy_html(html)
    for k, v in data.items():
        print(f"{k}: {str(v)[:100]}")

if __name__ == "__main__":
    main()