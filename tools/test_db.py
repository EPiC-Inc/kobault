"""Tests the layout of the database."""
# from dbapi import Database, Table

# db = Database()
# t = Table("Users")
# print(t.query("rowid,user_id,user_name"))
from objects import Characters

a = Characters.Pathfinder("a")
b = Characters.Pathfinder("b")
print(a.character_id)
print(b.character_id)
print(f"Eq: {a.character_id == b.character_id}")
