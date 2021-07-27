import sqlite3
from config import DATABASE_PATH

# If database hasn't been created, run gen_db.py
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
    query = ("INSERT INTO members (user_id, team) VALUES (?, ?)", [userid, teamid])
    _db_write(query)

def is_on_team(userid):
    query = ("SELECT COUNT(*) FROM members WHERE user_id=?", [userid])
    results = _db_read(query)
    return results[0][0] != 0

def get_team(userid):
    query = ("SELECT team FROM members WHERE user_id=?", [userid])
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
