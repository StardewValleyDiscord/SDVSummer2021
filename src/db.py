"""
Database layout:

teams(
    team_id      INT PRIMARY KEY
    team_name    TEXT
    points       INT
)

members(
    user_id     INT PRIMARY KEY
    team        INT
    FOREIGN KEY(team) REFERENCES teams(team_id)
    TODO: Add candy/tricks?
)
"""

import discord, sqlite3
from config import DATABASE_PATH

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
    query = ("INSERT INTO members (user_id, team) VALUES (?, ?)", [userid, teamid])
    _db_write(query)

def is_on_team(userid):
    query = ("SELECT COUNT(*) FROM members WHERE user_id=?", [userid])
    results = _db_read(query)
    return results[0][0] != 0
