import sqlite3


entries = [
    ('Task 1', '2023-03-01'),
    ('Task 2', '2023-02-26'),
    ('Task 3', '2023-04-23')
]

db_connection = sqlite3.connect("../../balancer_app.db")
cursor = db_connection.cursor()

cursor.executemany('''
    INSERT INTO tasks (text, due_date) VALUES (?, ?);
''', entries)

print('count: ', cursor.rowcount)

db_connection.commit()
db_connection.close()
