import sqlite3
from src.db.db_manager import DBManager
from src.util import utilities
import sys


def run_migrations():
    db_path = utilities.read_ini('DB', 'DB_PATH')
    migrations_db_path = utilities.read_ini('DB', 'MIGRATIONS_DB_PATH')
    db = DBManager(db_path)
    migrations_db = DBManager(migrations_db_path)

    migrations_db.create_migrations_table_id_not_exists()
    migrations = migrations_db.select_migrations_not_ran()

    for migration in migrations:
        migration_class_name = utilities.format_migration_class_name(migration[1])
        module = __import__('src.migrations.' + migration[1], None, None, [migration_class_name])
        cls = getattr(module, migration_class_name)

        try:
            cls(db).up()
            migrations_db.mark_migration_as_ran(int(migration[0]))
        except Exception as e:
            print(e)
