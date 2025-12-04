import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

with open("school.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()

print("school.db created using queries from school.sql")