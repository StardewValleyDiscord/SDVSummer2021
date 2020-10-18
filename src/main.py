# Autumn
# Discord bot made for the Fall 2020 SDV Discord event
# Written by aquova, 2020

import discord, traceback, os
import db, teams, trick_treat, utils
from config import SIGNUP_MES, CMD_PREFIX, DISCORD_KEY, DATABASE_PATH
from gen_db import init_db

client = discord.Client()

FUNC_DICT = {
    "add": teams.add_points,
    "lb": teams.print_lb,
    "tricks": trick_treat.list_trick_treat,
    "treats": trick_treat.list_trick_treat,
}

@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)

    if not os.path.exists(DATABASE_PATH):
        init_db()

@client.event
async def on_raw_reaction_add(payload):
    # If they have reacted to the specified message with the correct emoji, add the role
    if payload.message_id == SIGNUP_MES:
        await teams.signup_user(payload, client)
        return

    await trick_treat.trick_or_treat(payload, client)
    await teams.check_vote(payload, client)

@client.event
async def on_message(message):
    # Do not react to our own messages
    if message.author.id == client.user.id:
        return

    try:
        # Check if someone is using a bot command
        if message.content != "" and message.content[0] == CMD_PREFIX:
            prefix_removed = utils.strip_prefix(message.content)
            if prefix_removed == "":
                return
            command = utils.get_command(prefix_removed)

            if command in FUNC_DICT:
                output = await FUNC_DICT[command](message)
                if output != None:
                    await message.channel.send(output)
    except Exception as e:
        print(traceback.format_exc())

client.run(DISCORD_KEY)
