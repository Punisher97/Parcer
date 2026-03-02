from hhru_parser.methods.http import fetch_text, save_html

url = "https://hh.ru/vacancy/129527597?query=ML+Engineer+AND+NLP&hhtmFrom=vacancy_search_list"
html = fetch_text(url)
save_html(html, "debug/vacancy.html")
print("saved:", len(html))