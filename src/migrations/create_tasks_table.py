from src.migrations.migration import Migration


class CreateTasksTableMigration(Migration):
    def up(self):
        self.db_manager.create_task_table_id_not_exists()
