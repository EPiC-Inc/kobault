from pathlib import Path
from sqlite3 import connect

from objects import Characters

DB_LOCATION: str = str(Path("data/i.db"))
connection = connect(DB_LOCATION)
cols = {
    "character_id": "TEXT PRIMARY KEY"
}
for attribute in Characters.Pathfinder.__slots__:
    if not cols.get(attribute):
        cols[attribute] = "TEXT"

cols = [f"{col_name} {data_type}" for col_name, data_type in cols.items()]
table_command = f"CREATE TABLE IF NOT EXISTS Characters_Pathfinder({", ".join(cols)}) WITHOUT ROWID"

print(table_command)
# cursor = connection.cursor()
# cursor.execute(table_command)
# connection.commit()
