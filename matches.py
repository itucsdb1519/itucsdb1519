# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection

from store import StoreTeam

import psycopg2
import tournaments



def create_table():
    try:
        cursor = create_connection()
        statement = """ CREATE TABLE MATCHES(
        ID SERIAL PRIMARY KEY,
        TOURNAMENT INTEGER REFERENCES TOURNAMENTS ON DELETE CASCADE ON UPDATE CASCADE,
        TEAM1 INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
        TEAM2 INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
        SCORE VARCHAR(3)
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
        close_connection(cursor)
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        cursor.connection.close()

def get_matches():
    cursor = create_connection()

    cursor.execute("SELECT * FROM matches;")
    matches = cursor.fetchall()

    close_connection(cursor)

    return matches


def add_new_match(tournament, team1, team2, score):
    cursor = create_connection()

    cursor.execute("INSERT INTO matches (tournament, team1, team2, score) VALUES (%s, %s, %s, %s)", (tournament, team1, team2, score))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_match(id):
    cursor = create_connection()
    statement = """DELETE FROM MATCHES WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_match(tournamentFind, team1Find, team2Find, scoreFind):
    statement = """SELECT * FROM MATCHES WHERE ( CAST(TOURNAMENT AS VARCHAR(45)) LIKE '{}%' ) AND ( CAST(TEAM1 AS VARCHAR(45)) LIKE '{}%' ) AND ( CAST(TEAM2 AS VARCHAR(45)) LIKE '{}%' ) AND (SCORE LIKE '{}%')""".format(tournamentFind, team1Find, team2Find, scoreFind)

    cursor = create_connection()
    cursor.execute(statement)
    matches = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return matches

def update_match(id, tournamentUpdate, team1Update, team2Update, scoreUpdate):
    cursor = create_connection()
    statement = """UPDATE MATCHES SET TOURNAMENT = '{}', TEAM1 = '{}', TEAM2 = '{}', SCORE = '{}' WHERE ID={} """.format(tournamentUpdate, team1Update, team2Update, scoreUpdate, id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)
    
def showJointTables():
    cursor = create_connection()
    statement= """ SELECT MATCHES.ID, TOURNAMENTS.NAME, t1.NATION, t2.NATION, MATCHES.SCORE FROM MATCHES INNER JOIN TOURNAMENTS ON TOURNAMENTS.ID=MATCHES.TOURNAMENT INNER JOIN TEAMS t1 ON t1.ID = MATCHES.TEAM1 INNER JOIN TEAMS t2 ON t2.ID=MATCHES.TEAM2 """
    cursor.execute(statement)
    matches = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)
    return matches

def findInJointTables(tournamentFind, team1Find, team2Find, scoreFind):
    statement= """ SELECT MATCHES.ID, TOURNAMENTS.NAME, t1.NATION, t2.NATION, MATCHES.SCORE FROM MATCHES INNER JOIN TOURNAMENTS ON TOURNAMENTS.ID=MATCHES.TOURNAMENT INNER JOIN TEAMS t1 ON t1.ID=MATCHES.TEAM1 INNER JOIN TEAMS t2 ON t2.ID=MATCHES.TEAM2 WHERE(TOURNAMENTS.NAME LIKE  '{}%' ) AND (t1.NATION LIKE '{}%' ) AND (t2.NATION LIKE '{}%' )  AND (MATCHES.SCORE LIKE '{}%' )""".format(tournamentFind, team1Find, team2Find, scoreFind)

    cursor = create_connection()
    cursor.execute(statement)
    matches = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return matches

@app.route("/matches", methods=['GET', 'POST'])
def matches():

    #create_table()
    allTournaments = tournaments.get_tournaments()
    
    dsn = app.config['dsn']
    
    app.storeT = StoreTeam(dsn)
    allTeams = app.storeT.getAllTeams(dsn)

    if request.method == 'GET':
        all_matches = showJointTables() # get all matches
        queriedMatches = findInJointTables('?','?','?','?')

    elif 'add' in request.form:
        # ----------------------------------------------
        tournament = request.form['tournament']
        team1 = request.form['team1']
        team2 = request.form['team2']
        score = request.form['score']
        # ----------------------------------------------

        add_new_match(tournament, team1, team2, score) # save to db

        all_matches = showJointTables() # get all matches
        queriedMatches = findInJointTables('?','?','?','?')
    elif 'delete' in request.form:
        ids = request.form.getlist('matches_to_delete')
        for id in ids:
            delete_match(id)
        all_matches = showJointTables()
        queriedMatches = findInJointTables('?','?','?','?')
    elif 'find' in request.form:
        tournamentFind = request.form['tournamentFind']
        team1Find = request.form['team1Find']
        team2Find = request.form['team2Find']
        scoreFind = request.form['scoreFind']

        all_matches = showJointTables()
        queriedMatches = findInJointTables(tournamentFind, team1Find, team2Find, scoreFind)
    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            tournamentUpdate = request.form['tournamentUpdate'+id]
            team1Update = request.form['team1Update'+id]
            team2Update = request.form['team2Update'+id]
            scoreUpdate = request.form['scoreUpdate'+id]
            update_match(id, tournamentUpdate, team1Update, team2Update, scoreUpdate)

        all_matches = showJointTables()
        queriedMatches = findInJointTables('?','?','?','?')
    return render_template("matches.html", matches=all_matches, matchesToShow=queriedMatches, TournamentsSelect=allTournaments, TeamsSelect=allTeams)
