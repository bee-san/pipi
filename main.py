import discord
import asyncio

client = discord.Client()

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
        object = todo

class todo(object):
    """
    A todo list object. Will control the todolist. put in a class for neatness

    attributes(?)

    view_entries = reads all entries from SQL database

    add_entry = adds a new todo to the database

    delete entry = deletes entries 

    """

    import sqlite3

    db = sqlite3.connect("todo.db")
    c = db.cursor

    def __init__(self):
        db.create_tables([ToDo])


with open("token.txt") as token
token = token.read()

client.run('')


def good_morning(message):
