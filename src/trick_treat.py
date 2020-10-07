import discord
import db
from utils import Trick_Treat

async def trick_or_treat(payload, client):
    emoji_name = payload.emoji if type(payload.emoji) == str else payload.emoji.name

    tot = None
    if emoji_name == "🍬":
        tot = Trick_Treat.TREAT
    elif emoji_name == "🧅":
        tot = Trick_Treat.TRICK
    else:
        return

    sender = payload.user_id

    server = [x for x in client.guilds if x.id == payload.guild_id][0]
    channel = discord.utils.get(server.channels, id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    receiver = message.author.id

    sender_team = db.get_team(sender)
    receiver_team = db.get_team(receiver)
    if sender_team == receiver_team or sender_team == None or receiver_team == None:
        return

    if tot == Trick_Treat.TREAT:
        if db.use_trick_treat(sender, Trick_Treat.TREAT):
            db.add_points(receiver_team, 3)
            db.add_points(sender_team, 1)
    elif tot == Trick_Treat.TRICK:
        if db.use_trick_treat(sender, Trick_Treat.TRICK):
            db.add_points(receiver_team, -2)
            db.add_points(sender_team, -1)

async def list_trick_treat(message):
    tt = db.get_trick_treats(message.author.id)
    if tt == None:
        return "It looks like you haven't signed up for the event! Join a team to get some treats and tricks to use!"

    return f"You have {tt[0]} treats and {tt[1]} tricks remaining"
