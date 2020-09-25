import discord
import db, utils
from config import TEAMS, FALL2020_ROLE, FALL_ROLE

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

async def print_lb(message):
    out = '```\n'
    for team in TEAMS:
        out += f"{db.get_points(team['id'])} pts - {team['name']}\n"

    out += '```'
    return out

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
            fall_role = discord.utils.get(server.roles, id=FALL_ROLE)
            fall2020_role = discord.utils.get(server.roles, id=FALL2020_ROLE)
            user = discord.utils.get(server.members, id=payload.user_id)
            db.add_member(payload.user_id, team_id)
            await user.add_roles(new_role, fall2020_role, fall_role)
        except Exception as e:
            print(f"Something has gone wrong with adding team role: {e}")
