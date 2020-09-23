import discord
import db, utils
from config import TEAMS
from utils import Trick_Treat

@utils.requires_captain
async def add_points(message):
    mes = utils.remove_command(message.content).split(" ")
    team = [t for t in TEAMS if t['nick'].upper() == mes[0].upper()]
    if team:
        try:
            found_team = team[0]
            add_pts = int(mes[1])
            db.add_points(found_team['id'], add_pts)
            return f"{add_pts} points have been added to {found_team['name']}"
        except (ValueError, IndexError):
            return "You did not specify how many points to add"
    else:
        return "I could not find a team name in that message"

async def signup_user(payload, client):
    if db.is_on_team(payload.user_id):
        return

    team_emoji = [t for t in TEAMS if t['emoji'] == payload.emoji.name]
    if team_emoji:
        try:
            team = team_emoji[0]
            server = [x for x in client.guilds if x.id == payload.guild_id][0]
            team_id = team['id']
            new_role = discord.utils.get(server.roles, id=team_id)
            user = discord.utils.get(server.members, id=payload.user_id)
            db.add_member(payload.user_id, team_id)
            await user.add_roles(new_role)
        except Exception as e:
            print(f"Something has gone wrong with adding team role: {e}")

def trick_or_treat(payload, client, tot):
    sender = payload.user_id

    server = [x for x in client.guilds if x.id == payload.guild_id][0]
    channel = discord.utils.get(server.channels, id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    receiver = message.author.id

    sender_team = db.get_team(sender)
    receiver_team = db.get_team(receiver)
    if sender_team == receiver_team or sender_team == None:
        return

    if tot == Trick_Treat.TREAT:
        if db.use_trick_treat(sender, Trick_Treat.TREAT):
            db.add_points(receiver_team, 3)
            db.add_points(sender_team, 1)
    elif tot == Trick_Treat.TRICK:
        if db.use_trick_treat(sender, Trick_Treat.TRICK):
            db.add_points(receiver_team, -2)
            db.add_points(sender_team, -1)
