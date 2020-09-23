# Generates a newly created, initialized database

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
    treats      INT
    tricks      INT
)
"""

import sqlite3
from config import DATABASE_PATH, TEAMS

def main():
    sqlconn = sqlite3.connect(DATABASE_PATH)
    sqlconn.execute("CREATE TABLE teams (team_id INT PRIMARY KEY, team_name TEXT, points INT);")
    sqlconn.execute("CREATE TABLE members (user_id INT PRIMARY KEY, team INT, treats INT, tricks INT, FOREIGN KEY(team) REFERENCES teams(team_id));")

    for team in TEAMS:
        sqlconn.execute("INSERT INTO teams (team_id, team_name, points) VALUES (?, ?, ?)", [team['id'], team['name'], 0])

    sqlconn.commit()
    sqlconn.close()

if __name__ == "__main__":
    main()
