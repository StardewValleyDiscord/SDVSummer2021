import discord
import db, utils
from config import client, TEAMS, ROLE_CURRENT, ROLE_ANNUAL, VOTING_CHANNELS, LB_URL

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

@utils.requires_captain
async def print_lb(_):
    if LB_URL != "":
        return LB_URL
    else:
        out = '```\n'
        for team in TEAMS:
            out += f"{db.get_points(team['id'])} pts - {team['name']}\n"

        out += '```'
        return out

async def signup_user(payload):
    if db.is_on_team(payload.user_id):
        return

    emoji_name = payload.emoji if type(payload.emoji) == str else payload.emoji.name
    team_emoji = [t for t in TEAMS if t['emoji'] == emoji_name]
    if team_emoji:
        try:
            team = team_emoji[0]
            server = [x for x in client.guilds if x.id == payload.guild_id][0]
            user = discord.utils.get(server.members, id=payload.user_id)
            if team['capped']:
                channel = discord.utils.get(server.channels, id=payload.channel_id)
                message = await channel.fetch_message(id=payload.message_id)
                await message.remove_reaction(payload.emoji, user)
            else:
                team_id = team['id']
                new_role = discord.utils.get(server.roles, id=team_id)
                role_annual = discord.utils.get(server.roles, id=ROLE_ANNUAL)
                role_current = discord.utils.get(server.roles, id=ROLE_CURRENT)
                db.add_member(payload.user_id, team_id)
                await user.add_roles(new_role, role_current, role_annual)
        except Exception as e:
            print(f"Something has gone wrong with adding team role: {e}")

async def check_vote(payload):
    emoji_name = payload.emoji if type(payload.emoji) == str else payload.emoji.name

    if emoji_name != "☑️":
        return

    server = [x for x in client.guilds if x.id == payload.guild_id][0]
    channel = discord.utils.get(server.channels, id=payload.channel_id)
    if channel.id not in VOTING_CHANNELS:
        return

    reactor_team = db.get_team(payload.user_id)
    if reactor_team == None:
        return
    message = await channel.fetch_message(id=payload.message_id)
    poster_team = db.get_team(message.author.id)
    if reactor_team == poster_team:
        reactor = discord.utils.get(server.members, id=payload.user_id)
        await message.remove_reaction(payload.emoji, reactor)
