# Internal
import asyncio
import json
import logging
import datetime
import time

# External
import discord
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
client = discord.Client()
client_wit = Wit(token_wit)

logging.basicConfig(level=logging.INFO)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        # test call
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('!pipi') or message.content.startswith('pipi'):
        # responds to !pipi or pipi
        data = client_wit.message(remove_pipi_msg(message.content))
        if "reminder" in data["entities"]:
            logging.info("In reminder")
            # gets reminder details if "reminder" is found in feedback
            try:
                reminder_value = data["entities"]["reminder"][0]["value"]
                reminder_confidence = data["entities"]["reminder"][0]["confidence"]
            except KeyError:
                logging.debug("#164 dictionary does not contain right items")
        if "datetime" in data["entities"]:
            logging.info("In datetime")
            # gets datetime details if "datetime" is found in feedback
            try:
                datetime_value = data["entities"]["datetime"][0]["value"]
                datetime_confidence = data["entities"]["datetime"][0]["confidence"] 
            except KeyError:
                logging.debug("#764 dictionary does not contain right items")
        else:
            # reminders always need dates, so if one isn't then datetime set to current time + 24hrs
            datetime_value = get_date_tomorrow()
        print(reminder_confidence)
        if reminder_confidence > 0.9:
            logging.info("Determind to be a reminder")
            await client.send_message(message.channel, ("Your data is {} with confidence {} and datetime {} and confidence {}".format(reminder_value, reminder_confidence, datetime_value, "datetime_confidence")))

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

# learn classes
# Learn SQLlite

#############################################################################################################
# ToDo #
def ToDo(reminder_value, datetime_value):
    print("yes, this works.")
    return
    """
    import sqlite3    
    con = sqlite3.connect('todo.db') # Warning: This file is created in the current directory
    con.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(250) NOT NULL, date TEXT, reminder_date TEXT)")
    return con"""

def ToDo_add(message, con):
    import datetime
    from random import randint
    con.execute("""INSERT INTO ToDo(id, task, date, reminder_date)
    VALUES(?, ?, ?, ?)""", (id, task, (datetime), reminder_date))
    con.commit()



client.run(token_discord)
