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



def ToDo_add(task, datetime1, con):
	# Adds new entry to todo table.
	from datetime import datetime
	from random import randint

	con.execute("""INSERT INTO todo(task, datetime, addedWhen) VALUES (?, ?, ?)""", (task, datetime1, (datetime.now())))


	return

