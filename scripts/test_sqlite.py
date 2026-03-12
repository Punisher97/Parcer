import sqlite3

conn = sqlite3.connect("hh.sqlite")
cursor = conn.cursor()

cursor.execute("SELECT * FROM vacancies")

print(cursor.fetchall())