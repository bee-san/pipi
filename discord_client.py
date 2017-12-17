# Internal
import asyncio
import json
import logging
import datetime
import time

# External
import discord

logging.basicConfig(filename='PiPiLog.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

# Getting API tokens
with open("token.txt") as file:
    file_read = file.readlines()
    token_discord = file_read[0].split()
    token_discord = token_discord[1]

    token_wit = file_read[1].split()
    token_wit = token_wit[1]

client = discord.Client()

@client.event
async def on_ready(message):
    await client.send_message(message.channel, message)

@client.event
async def on_message(message):
    if message.content.startswith('!pipi or pipi'):
        import main.py
        reply = parse_data(message)
        await client.send_message(message.channel, reply)


def remove_pipi_msg(message):
    # removes "pipi" or "!pipi" from front of message so wit.ai can process it
    if message.startswith("!pipi"):
        return message[6:]
    else:
        return message[5:]

client.run(token_discord)