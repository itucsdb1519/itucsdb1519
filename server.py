import datetime
import json
import os
import re

from config import create_connection
from config import close_connection

from flask import Flask
from flask import render_template

from config import app


import coaches
import referees
import tournaments
import players
import teams
import users
import matches
import matchstatistics
from store import StoreTM
from store import StoreP
from store import StoreTeam


import technicmembers




def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

@app.route('/uninitializeDatabase')
def uninitDb():
    statement="""DROP TABLE MATCHES, PLAYERS, COACHES, REFEREES, TEAMS, TOURNAMENTS, USERS, MATCHSTATISTICS, TECHNICMEMBERS"""
    cursor = create_connection()
    cursor.execute(statement)
    cursor.connection.commit()
    close_connection(cursor)
    return render_template('home.html')

@app.route('/initializeDatabase')
def initDb():
    app.storeTeams = StoreTeam(app.config['dsn'])
    app.storeTeams.createTable(app.config['dsn'])
    app.storeTeams.createInitTeams(app.config['dsn'])
    coaches.create_table()
    app.storePlayers = StoreP(app.config['dsn'])
    app.storePlayers.createTable(app.config['dsn'])
    app.storePlayers.createInitPlayers(app.config['dsn'])
    tournaments.create_table()
    referees.create_table()
    users.create_table()
    matches.create_table()
    matchstatistics.create_table()
    app.store = StoreTM(app.config['dsn'])
    app.store.createTable(app.config['dsn'])

    return render_template('home.html')

@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

if __name__ == '__main__':


    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=54321 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=int(PORT))
