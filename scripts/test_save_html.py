from hhru_parser.methods.http import save_html

html = "<h1>Test</h1>"
path = "debug/test.html"

save_html(html, path)

print("Done")