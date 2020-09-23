import discord, sqlite3
from config import DATABASE_PATH, INIT_TREATS, INIT_TRICKS
from utils import Trick_Treat

# If database hasn't been created, run scripts/gen_db.py

def _db_read(query):
    sqlconn = sqlite3.connect(DATABASE_PATH)
    results = sqlconn.execute(*query).fetchall()
    sqlconn.close()

    return results

def _db_write(query):
    sqlconn = sqlite3.connect(DATABASE_PATH)
    sqlconn.execute(*query)
    sqlconn.commit()
    sqlconn.close()

def add_member(userid, teamid):
    # TODO: May want to catch foreign key SQLite exceptions (which shouldn't be possible)
    query = ("INSERT INTO members (user_id, team, treats, tricks) VALUES (?, ?, ?, ?)", [userid, teamid, INIT_TREATS, INIT_TRICKS])
    _db_write(query)

def is_on_team(userid):
    query = ("SELECT COUNT(*) FROM members WHERE user_id=?", [userid])
    results = _db_read(query)
    return results[0][0] != 0

def get_team(userid):
    query = ("SELECT teamid FROM members WHERE user_id=?", [userid])
    results = _db_read(query)
    try:
        return results[0][0]
    except IndexError:
        return None

def add_points(teamid, pts):
    old_pts_query = ("SELECT * FROM teams WHERE team_id=?", [teamid])
    old_pts = _db_read(old_pts_query)[0]
    new_pts = old_pts[2] + pts
    update_query = ("REPLACE INTO teams (team_id, team_name, points) VALUES (?, ?, ?)", [teamid, old_pts[1], new_pts])
    _db_write(update_query)

def get_points(teamid):
    query = ("SELECT points FROM teams WHERE team_id=?", [teamid])
    pts = _db_read(query)
    try:
        return pts[0][0]
    except IndexError:
        return None

def get_trick_treats(userid):
    fetch_query = ("SELECT treats, tricks FROM members WHERE user_id=?", [userid])
    results = _db_read(fetch_query)
    try:
        return results[0]
    except IndexError:
        return None

def use_trick_treat(userid, tot):
    fetch_query = ("SELECT * FROM members WHERE user_id=?", [userid])
    results = _db_read(fetch_query)
    if not results:
        return

    if tot == Trick_Treat.TREAT:
        # If user is out of treats, just leave
        if results[0][2] == 0:
            return False
        results[2] -= 1
    elif tot == Trick_Treat.TRICK:
        # If user is out of tricks, leave
        if results[0][3] == 0:
            return False
        results[3] -= 1

    replace_query = ("REPLACE INTO members (user_id, team, treats, tricks) VALUES (?, ?, ?, ?)", results)
    _db_write(replace_query)
    return True
