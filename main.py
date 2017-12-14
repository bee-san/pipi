# Internal
import asyncio
import json
import logging


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
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('!pipi') or message.content.startswith('pipi'):
        data = client_wit.message(remove_pipi_msg(message.content))
        if "reminder" in data["entities"]:
            try:
                reminder_value = data["entities"]["reminder"][0]["value"]
                reminder_confidence = data["entities"]["reminder"][0]["confidence"]
            except KeyError:
                logging.debug("#164 dictionary does not contain right items")
        if "datetime" in data["entities"]:
            print("\n\n\nreached datetime\n\n\n")
            try:
                datetime_value = data["entities"]["datetime"][0]["value"]
                datetime_confidence = data["entities"]["datetime"][0]["confidence"] #a
            except KeyError:
                logging.debug("#764 dictionary does not contain right items")
        await client.send_message(message.channel, ("Your data is {} with confidence {} and datetime {} and confidence {}".format(reminder_value, reminder_confidence, datetime_value, datetime_confidence)))

    elif message.content.startswith('!todo'):
        ToDo()


def remove_pipi_msg(message):
    if message.startswith("!pipi"):
        return message[6:]
    else:
        return message[5:]

# learn classes
# Learn SQLlite

#############################################################################################################
# ToDo #
def ToDo():
    import sqlite3    
    con = sqlite3.connect('todo.db') # Warning: This file is created in the current directory
    con.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(250) NOT NULL, date TEXT, reminder_date TEXT)")
    return con

def ToDo_add(message, con):
    import datetime
    from random import randint
    con.execute("""INSERT INTO ToDo(id, task, date, reminder_date)
    VALUES(?, ?, ?, ?)""", (id, task, (datetime.datetime.now), reminder_date))
    con.commit()



client.run(token_discord)
