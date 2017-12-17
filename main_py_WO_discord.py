# Internal
import logging

# External
from wit import Wit

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

def main():
	while True:
		message = input("> ")
		parse_data(message)

def parse_data(message):
	# use signal for this. Consider developing your own interpretations?
	data = client_wit.message(message)
	logging.info(data)
	def parse_reminder(message):
		logging.info("In reminder")
		# gets reminder details if "reminder" is found in feedback
		try:
			reminder_value = data["entities"]["reminder"][0]["value"]
			reminder_confidence = data["entities"]["reminder"][0]["confidence"]
		except KeyError:
			logging.debug("#164 dictionary does not contain right items")
		if "datetime" in data["entities"]:
			datetime_value = parse_datetime(message)
		else:
			datetime_value = get_date_tomorrow()
		return(reminder_value, reminder_confidence, datetime_value)

	def parse_datetime(data):
		logging.info("In datetime")
		try:
			datetime_value = data["entities"]["datetime"][0]["value"]
			datetime_confidence = data["entities"]["datetime"][0]["confidence"]
		except KeyError:
			logging.debug("#764 dictionary does not contain right items")

		return(datetime_value, datetime_confidence)

	def parse_debug(data):
		logging.info("in debug")

	if "reminder" in data["entities"]:
		todo_var = parse_reminder(data)
		ToDo(todo_var)
		print("Your reminder has been set")
		return("Your reminder has been set.")



def get_date_tomorrow():
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
	# removes "pipi" or "!pipi" from front of message so wit.ai can process it
	if message.startswith("!pipi"):
		return message[6:]
	else:
		return message[5:]

#############################################################################################################
# ToDo #
def ToDo(reminder_tuple):
	import database_handler

	logging.info(reminder_tuple)

	table_name = "todo"
	db_handler = database_handler.Database_controller(table_name)

	db_handler.cursor.execute("""CREATE TABLE IF NOT EXISTS
		todo(id INTEGER PRIMARY KEY, task TEXT,
		datetime TEXT, addedWhen TEXT)""")

	reminder_value = reminder_tuple[0]
	reminder_confidence = reminder_tuple[1]
	reminder_Datetime = reminder_tuple[2]

	database_handler.ToDo_add(reminder_value, reminder_Datetime, db_handler.cursor)

	logging.info("task has been added to database")

	db_handler.db.commit()


main()
