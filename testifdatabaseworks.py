import sqlite3
connection = sqlite3.connect("test.db")
print(connection.total_changes)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS example (id INTEGER, name TEXT, age INTEGER)")
cursor.execute("INSERT INTO example VALUES (1, 'alice', 20)")
cursor.execute("INSERT INTO example VALUES (2, 'bob', 30)")
cursor.execute("INSERT INTO example VALUES (3, 'eve', 40)")
cursor.execute("SELECT * FROM example")
rows = cursor.fetchall()
for row in rows:
    print(row)
connection.commit()