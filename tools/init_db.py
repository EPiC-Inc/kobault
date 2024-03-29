"""Initializes the database with the proper columns."""
from sys import path
from pathlib import Path
from sqlite3 import connect

path.append("../kobault")

from objects import User, Characters


DB_LOCATION: str = str(Path("data/i.db"))


def gen_command(object_: object, object_name: str, alterations: dict | None = None):
    cols = {}
    try:
        attributes = object_.__slots__  # type: ignore
    except AttributeError:
        attributes = object_.__dict__
    for attribute in attributes:
        cols[attribute] = "TEXT"

    if alterations and (alterations_items := alterations.items()):
        for alt_col, alt_data in alterations_items:
            cols[alt_col] = alt_data

    cols = [f"{col_name} {data_type}" for col_name, data_type in cols.items()]
    table_command = f"CREATE TABLE IF NOT EXISTS {object_name.replace('.', '_')}({', '.join(cols)}) WITHOUT ROWID"
    return table_command


objects = [User, Characters.Pathfinder]
object_names = ["Users", "Characters.Pathfinder"]
alterations = [
    {"user_id": "TEXT PRIMARY KEY", "password": "BLOB"},
    {
        "user_id": 'TEXT NOT NULL REFERENCES "Users"("user_id")',
        "character_id": "TEXT PRIMARY KEY",
    },
]

for o, name, alts in zip(objects, object_names, alterations):
    table_command = gen_command(o, name, alts)
    print(table_command)

    connection = connect(DB_LOCATION)
    cursor = connection.cursor()
    cursor.execute(table_command)
    connection.commit()
