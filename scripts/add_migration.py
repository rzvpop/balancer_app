import sys
from util import utilities
import sqlite3
import functools


if len(sys.argv) < 2:
    exit('Not enough arguments')

db_connection = sqlite3.connect(utilities.read_ini('DB', 'DB_PATH'))
cursor = db_connection.cursor()

cursor.execute('''
    INSERT INTO migrations(name) VALUES (?)
''', [sys.argv[1]])

class_name = utilities.format_migration_class_name(sys.argv[1])
with open('src/migrations/' + sys.argv[1] + '.py', 'w') as file:
    file.write('''from src.migrations.migration import Migration


class {}(Migration):
    def up(self):
        pass
    '''.format(class_name))

db_connection.commit()
db_connection.close()


