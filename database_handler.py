# Module to handle database interactions, mainly for ToDo but could be used for others.


###############################
# ToDo
###############################


import sqlite3
with sqlite3.connect('todo.db') as db:
		pass

class Database_controller():
	"""
	Class which handles database stuff. Objects are instantiated with table names
	so one object per table.

	*Values*
	self.cursor = SQLite cursor
	self.db = SQLite db

	"""
	def __init__(self, table_name):
		self.cursor = db.cursor()
		self.db = db

def ToDo_create():
	db_handler = Database_controller("todo.db")
	db_handler.cursor.execute("""CREATE TABLE IF NOT EXISTS
		todo(id INTEGER PRIMARY KEY, task TEXT,
		datetime TEXT, addedWhen TEXT)""")

def ToDo_add(tuple):
	# Adds new entry to todo table.
	from datetime import datetime
	from random import randint

	task = tuple[0]
	datetime1 = tuple[2]

	db_handler = Database_controller("todo.db")
	db_handler.cursor.execute("""INSERT INTO todo(task, datetime, addedWhen) VALUES (?, ?, ?)""", (task, datetime1, (datetime.now())))


	return

def ToDo_view():
	from pprint import pprint
	db_handler = Database_controller("todo.db")
	db_handler.cursor.execute("""SELECT * FROM todo""")
	names = [description[0] for description in db_handler.cursor.description]
	values = db_handler.cursor.fetchall()

	print("id\ttask")
	print("-"*10)

	for i in values:
		print(str(i[0]) + "\t" + i[1])

	# pprint(db_handler.cursor.fetchall())

