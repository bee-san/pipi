# Built into Python
import logging
import datetime
import sqlite3
import requests

# External
from wit import Wit
import arrow

logging.basicConfig(filename='PiPiLog.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

# Getting API tokens
with open("token.txt") as file:
	file_read = file.readlines()
	token_wit = file_read[1].split()

# Setting up clients
client_wit = Wit(token_wit[1])

logging.basicConfig(level=logging.INFO)


# logging.disable(logging.CRITICAL) 


def main():
	while True:
		message = input("> ")
		parse_data(message)


def parse_data(message):
	# use signal for this. Consider developing your own interpretations?
	data = client_wit.message(message)
	logging.info(data)

	def parse_command(message):
		logging.info("in parse command")
		logging.info(message)
		print(message)
		if "DEBUG" or "!DEBUG" in message.upper():
			#TODO get debug to work
			print("Debug mode has been activated.")
		elif "HELP" or "!HELP" in message.upper():
			print(help_menu())
			return("help mode has been sent")

	def parse_reminder(message):
		logging.info("In reminder")
		# gets reminder details if "reminder" is found in feedback
		try:
			reminder_value = data["entities"]["reminder"][0]["value"]
			reminder_confidence = data["entities"]["reminder"][0]["confidence"]
			logging.info(reminder_value)
			logging.info(reminder_confidence)
		except KeyError:
			logging.debug("#164 dictionary does not contain right items")
		if "datetime" in data["entities"]:
			datetime_value = parse_datetime(message)
			datetime_value = datetime_value[0]
		else:
			datetime_value = get_date_tomorrow()
			logging.info("got tomorrows date")
		
		logging.info("finished reminder")
		return(reminder_value, reminder_confidence, datetime_value)

	def parse_datetime(data):
		logging.info("In datetime")
		try:
			datetime_value = data["entities"]["datetime"][0]["value"]
			datetime_confidence = data["entities"]["datetime"][0]["confidence"]
		except KeyError:
			logging.debug("#764 dictionary does not contain right items")

		return(datetime_value, datetime_confidence)

	def parse_show_me(data):
		logging.info(data)
		# I dont know why I need this import statement, but code breaks otherwise
		show_what_data = data["entities"]["show_me"][0]["entities"]["show_what"][0]["value"]
		show_what_confi = data["entities"]["show_me"][0]["entities"]["show_what"][0]["confidence"]
		if show_what_confi < 0.85:
			return("Show me failed.")
		else:
			if "TODO" or "REMINDER" in show_what_data.upper():
				show = ToDo_view()
		return show

	if message.startswith("!"):
		logging.info("in command")
		parse_command(message)
		return("this was a command")

	elif "reminder" in data["entities"]:
		logging.info("in reminder first part")
		todo_tuple = parse_reminder(data)
		logging.info(todo_tuple)
		if todo_tuple[1] < 0.85:
			print("This is not a reminder.")
			logging.info("this is not a reminder")
			return("this is not a reminder")
		else:
			ToDo_create()
			ToDo_add(parse_reminder(data))
			logging.info("yeah it worked")
			print("Your reminder has been set")
			return("Your reminder has been set.")
	elif "show_me" in data["entities"]:
		show_me = parse_show_me(data)
		return show_me


def help_menu():
	message = """
	Hello and welcome to the help menu.
	This project was created by Brandon Skerritt in December 2017.
	This project is under an MIT license.
	"""
	return message

def get_date_tomorrow():
	logging.info("in get date tomorrow")
	# can modify so you can choose own time
	from datetime import datetime, timedelta
	import time
	# Get today's datetime
	dtnow = datetime.now()
	# Create datetime variable for 6 AM
	dt6 = None
	# Get 1 day duration to add
	day = timedelta(days=1)
	# Generate tomorrow's datetime
	tomorrow = dtnow + day
	# Create new datetime object using tomorrow's year, month, day at 6 AM
	dt6 = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 12, 0, 0, 0)
	# Create timestamp from datetime object
	timestamp = time.mktime(dt6.timetuple())
	return(timestamp)

def remove_pipi_msg(message):
	logging.info("in remove_pipi message")
	# removes "pipi" or "!pipi" from front of message so wit.ai can process it
	if message.startswith("!pipi"):
		return message[6:]
	else:
		return message[5:]

#############################################################################################################
# ToDo #

## ToDo Class and controller ###
class Database_controller():
	"""
	Class which handles database stuff. Objects are instantiated with table names
	so one object per table.

	*Values*
	self.cursor = SQLite cursor
	self.db = SQLite db

	"""
	def __init__(self, table_name):
		self.db = sqlite3.connect(table_name)
		self.cursor = self.db.cursor()

#####################################
ToDo = Database_controller("todo.db")
#########################

def ToDo_create():
	# uses database object defined at top of file. creates new table
	ToDo.cursor.execute("""CREATE TABLE IF NOT EXISTS
		todo(id INTEGER PRIMARY KEY, task TEXT,
		datetime TEXT, addedWhen TEXT, done INTEGER)""")
	ToDo.db.commit()

def ToDo_add(tuple):
	# uses database object at top of file
	# Adds new entry to todo table.
	task = tuple[0]
	datetime1 = tuple[2]
	logging.info("just about to add a new reminder")
	ToDo.cursor.execute("""INSERT INTO todo(task, datetime, addedWhen, done) VALUES (?, ?, ?, ?)""", (task, datetime1, (str(arrow.now())), 0))
	ToDo.db.commit()
	return

def ToDo_get_age(age):
	age_arrow = arrow.get(age)
	return age_arrow.humanize()

def ToDo_when_due(due):
	present = arrow.utcnow()
	due = arrow.get(due)
	
	return due.humanize(present)


def ToDo_view():
	return_list = []
	# This will be what this function returns.
	# view the ToDo table
	ToDo.cursor.execute("""SELECT * FROM todo WHERE done = 0""")
	values = ToDo.cursor.fetchall()

	# gets a list of every single task
	list_of_tasks = map(lambda x: x[1], values)

	# names is every single column name
	names = [description[0] for description in ToDo.cursor.description]

	# gets a list of all tasks
	longest_task = (len(max(list_of_tasks, key=len)) - 4)
	spaces = (" " * (longest_task + 4))
	# gets how many spaces the longest task is
	string_top = ("id\ttask{}due\t\tage".format(spaces))
	return_list.append(string_top)
	# 10 + spaces + 3 + 8
	print(string_top)
	# formarts it so the due column isn't direclty over the longest task
	string_lines = ("-"*20) 
	print(string_lines)
	return_list.append(string_lines)

	for i in values:
		task_len = len(i[1])
		# gets current task length
		if not task_len == longest_task:
			# if the current task is not the longest task
			fill_length = len(spaces) - task_len + 4
			# find out how much space is between task and "due" column, then print it with that much space
		else:
			fill_length = 4
			# else just print it with a tab between them
		due = ToDo_when_due(i[2])
		due_len = len(due)
		space_age_due = (" " * (12 - due_len))
		output = (str(i[0]) + "\t" + str(i[1]) + (fill_length * " ") + ToDo_when_due(i[2]) + space_age_due + ToDo_get_age(i[3]))
		print(output)
		return_list.append(output)

	return ("\n".join(return_list))
		

################################################################
# GOOD MORNING
###################################################

def GoodMorning():
	# weather
	# top 3 HN links
	# /r/hacking /r/python /r/bitcoin
	# current crypto prices (use library)?
	# any emails i've received
	# my todo list
	# an inspirational quote
	
	return("Hello")


main()
