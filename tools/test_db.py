"""Tests the layout of the database."""
from dbapi import Database, Table

db = Database()
t = Table("Users")
print(t.query("rowid,user_id,user_name"))
