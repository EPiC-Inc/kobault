"""Abstraction module to interact with the database."""

from pathlib import Path
from sqlite3 import connect
from threading import Lock

DB_PATH = Path("data/i.db")
if not DB_PATH.exists():
    with open(DB_PATH, "w", encoding=None):
        pass


class Database:
    database: str
    lock: Lock

    def __init__(self) -> None:
        Database.database = str(DB_PATH)
        Database.lock = Lock()


class Table:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def query(
        self, columns, where_column: str | None = None, where_data: list | None = None
    ) -> list:
        """Queries the table's current data."""
        Database.lock.acquire()
        with connect(Database.database) as connection:
            cursor = connection.cursor()
            if where_column and where_data:
                result = cursor.execute(
                    f"SELECT {columns} FROM {self.name} WHERE {where_column} = ?",
                    where_data,
                )
            else:
                result = cursor.execute(f"SELECT {columns} FROM {self.name}")
        Database.lock.release()
        return [*result]

    def insert(self, values, *, lock_needed: bool = True) -> None:
        """Inserts <values> into the current table."""
        if lock_needed:
            Database.lock.acquire()
        with connect(Database.database) as connection:
            cursor = connection.cursor()
            command = f"INSERT INTO {self.name} VALUES({('?, ' * len(values))[:-2]})"
            cursor.execute(command, values)
            connection.commit()
        if lock_needed:
            Database.lock.release()

    def update_property(
        self,
        property_column: str,
        property_data: str,
        where_column: str,
        where_data: str,
    ) -> None:
        """Updates a SINGLE property."""
        Database.lock.acquire()
        with connect(Database.database) as connection:
            cursor = connection.cursor()
            command = f"UPDATE {self.name} SET {property_column} = ? WHERE {where_column} = ?"
            cursor.execute(command, [str(property_data), str(where_data)])
            connection.commit()
        Database.lock.release()


    def insert_object(self, object_) -> None:
        """Inserts an object or its properties into the current table."""
        Database.lock.acquire()
        try:
            data = object_.__dict__
            if not data:
                data = object_.__slots__
        except AttributeError:
            data = object_.__slots__
        self.insert([str(getattr(object_, attr)) for attr in data], lock_needed=False)
        Database.lock.release()
