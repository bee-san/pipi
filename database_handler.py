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
	db_handler.db.commit()

def ToDo_add(tuple):
	# Adds new entry to todo table.
	from datetime import datetime
	from random import randint
	task = tuple[0]
	datetime1 = tuple[2]
	db_handler = Database_controller("todo.db")
	db_handler.cursor.execute("""INSERT INTO todo(task, datetime, addedWhen) VALUES (?, ?, ?)""", (task, datetime1, (arrow.now())))
	db_handler.db.commit()
	return

def ToDo_view():
	from pprint import pprint
	db_handler = Database_controller("todo.db")
	db_handler.cursor.execute("""SELECT * FROM todo""")
	values = db_handler.cursor.fetchall()
	# names is every single column name
	names = [description[0] for description in db_handler.cursor.description]

	# gets a list of all tasks
	list_of_tasks = []
	for i in values:
		list_of_tasks.append(i[1])

	longest_task = (len(max(list_of_tasks, key=len)) - 4)
	# gets the length of the longest task - a tab length
	spaces = (" " * longest_task)
	# gets how many spaces the longest task is
	print("id\ttask{}due\tage".format(spaces))
	# formarts it so the due column isn't direclty over the longest task
	print("-"*10)

	for i in values:
		# prints the values of things
		print(str(i[0]) + " " + str(i[1]) + "\t")


ToDo_view()
"""
def ToDo_view():
	from pprint import pprint
	import time
	import calendar
	db_handler = Database_controller("todo.db")
	db_handler.cursor.execute
	names = [description[0] for description in db_handler.cursor.description]
	values = db_handler.cursor.fetchall()
	print(values)

	print("id\ttask\tage")
	print("-"*10)

	for i in values:
		# prints the id number, the task and the age of the task
		# TODO work on this.
		print(str(i[0]) + "\t" + i[1] + "\t" + str(int((float(calendar.timegm(time.gmtime())) - float(i[2])))) + "s")

	# pprint(db_handler.cursor.fetchall())

"""