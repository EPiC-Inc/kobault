"""Abstraction module to interact with the database."""

from pathlib import Path
from sqlite3 import connect

DB_PATH = Path("data/i.db")
if not DB_PATH.exists():
    with open(DB_PATH, "w", encoding=None):
        pass


class Database:
    database: str

    def __init__(self) -> None:
        Database.database = str(DB_PATH)


class Table:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def query(
        self, columns, where_column: str | None = None, where_data: list | None = None
    ) -> list:
        """Queries the table's current data."""
        with connect(Database.database) as connection:
            cursor = connection.cursor()
            if where_column and where_data:
                result = cursor.execute(
                    f"SELECT {columns} FROM {self.name} WHERE {where_column} = ?",
                    where_data,
                )
            else:
                result = cursor.execute(f"SELECT {columns} FROM {self.name}")
        return [*result]

    def insert(self, values) -> None:
        """Inserts <values> into the current table.
        Not currently implemented.
        """
        with connect(Database.database) as connection:
            cursor = connection.cursor()
            command = f"INSERT INTO {self.name} VALUES({('?, ' * len(values))[:-2]})"
            print(command)
            print(values)
            cursor.execute(command, values)
            connection.commit()

    def update(self) -> None:
        """Not currently implemented."""
        pass

    def insert_object(self, object_) -> None:
        """Inserts an object or its properties into the current table."""
        # Database.database.insert(object_)
        # Database.database.commit()
