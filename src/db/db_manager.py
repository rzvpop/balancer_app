import sqlite3


def establish_connection(f):
    def wrapper(self_copy, *args, **kwargs):
        connection = sqlite3.connect(self_copy.get_db_name())
        cursor = connection.cursor()

        try:
            return f(self_copy, cursor, *args)
        except Exception as e:
            raise e
        finally:
            connection.commit()
            connection.close()

    return wrapper


class DBManager:
    def __init__(self, db_name):
        self._db_name = db_name

    def get_db_name(self):
        return self._db_name

    @establish_connection
    def select_tasks(self, cursor):
        cursor.execute("SELECT * FROM tasks")
        records = cursor.fetchall()

        return records

    @establish_connection
    def insert_task(self, cursor, entry):
        cursor.execute("INSERT INTO tasks(text, due_date) VALUES (?, ?)", entry)

    @establish_connection
    def create_task_table_id_not_exists(self, cursor):
        cursor.execute('''
            CREATE TABLE tasks(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [text] TEXT,
                [due_date] INTEGER
            )
        ''')

    @establish_connection
    def create_migrations_table_id_not_exists(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS migrations (
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [name] TEXT UNIQUE NOT NULL,
                [ran] INTEGER DEFAULT 0 
            )
        ''')

    @establish_connection
    def select_migrations_not_ran(self, cursor):
        cursor.execute('''
            SELECT * FROM migrations WHERE ran=0 ORDER BY id
        ''')
        migrations = cursor.fetchall()

        return migrations if migrations is not None else []

    @establish_connection
    def mark_migration_as_ran(self, cursor, migration_id):
        cursor.execute('''
            UPDATE migrations SET ran=1 WHERE id=?
        ''', [migration_id])
