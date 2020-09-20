import discord
import db, utils
from config import TEAMS

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
