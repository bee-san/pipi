# Built into Python
import logging
import datetime

# External
from wit import Wit

# Internal modules
import database_handler

logging.basicConfig(filename='PiPiLog.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

# Getting API tokens
with open("token.txt") as file:
	file_read = file.readlines()
	token_discord = file_read[0].split()
	token_discord = token_discord[1]

	token_wit = file_read[1].split()
	token_wit = token_wit[1]

# Setting up clients
client_wit = Wit(token_wit)

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
		import database_handler
		print(message)
		if "DEBUG" or "!DEBUG" in message.upper():
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
		import database_handler
		# I dont know why I need this import statement, but code breaks otherwise
		show_what_data = data["entities"]["show_me"][0]["entities"]["show_what"][0]["value"]
		show_what_confi = data["entities"]["show_me"][0]["entities"]["show_what"][0]["confidence"]
		if show_what_confi < 0.85:
			return("this failed")
		else:
			if "TODO" or "REMINDER" in show_what_data.upper():
				database_handler.ToDo_view()

	if message.startswith("!"):
		logging.info("in command")
		parse_command(message)
		return("this was a command")

	elif "reminder" in data["entities"]:
		logging.info("in reminder first part")
		todo_tuple = parse_reminder(data)
		logging.info(todo_tuple)
		if todo_tuple[1] == 0.00001:
			logging.info("this is not a reminder")
			return("this is not a reminder")
		else:
			import database_handler
			database_handler.ToDo_create()
			database_handler.ToDo_add(parse_reminder(data))
			logging.info("yeah it worked")
			print("Your reminder has been set")
			return("Your reminder has been set.")
	elif "show_me" in data["entities"]:
		parse_show_me(data)


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
"""
def ToDo(reminder_tuple):


	reminder_value = reminder_tuple[0]
	reminder_confidence = reminder_tuple[1]
	reminder_Datetime = reminder_tuple[2]

	database_handler.ToDo_add(reminder_value, reminder_Datetime, db_handler.cursor)

	logging.info("task has been added to database")

	db_handler.db.commit()

"""
main()
