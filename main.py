# Internal
import asyncio

# External
import discord
from wit import Wit


# Getting API tokens
with open("token.txt") as file:
    file_read = file.readlines()
    token_discord = file_read[0].split()
    token_discord = token_discord[1]

    token_wit = file_read[1].split()
    token_wit = token_wit[1]


client = discord.Client()

# Setting up WIT
# client = Wit(token_wit)


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
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!todo'):
        ToDo()


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
    from random import randint
    con.execute("""INSERT INTO ToDo(id, task, date, reminder_date)
    VALUES(?, ?, ?, ?)""", (id, task, (import datetime; datetime.datetime.now), reminder_date))
    con.commit()



client.run(token_discord)
