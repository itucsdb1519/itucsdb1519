# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection

from store import StoreP

import psycopg2
import players
import teams



def create_table():
    try:
        cursor = create_connection()
        statement = """ CREATE TABLE TOURNAMENTS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        YEAR VARCHAR(4),
        WINNER INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
        BEST_PLAYER INTEGER REFERENCES PLAYERS ON DELETE CASCADE ON UPDATE CASCADE
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
        close_connection(cursor)
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        cursor.connection.close()

def get_tournaments():
    cursor = create_connection()

    cursor.execute("SELECT * FROM tournaments;")
    tournaments = cursor.fetchall()

    close_connection(cursor)

    return tournaments


def add_new_tournament(name, year, winner, best_player):
    cursor = create_connection()

    cursor.execute("INSERT INTO tournaments (name, year, winner, best_player) VALUES (%s, %s, %s, %s)", (name, year, winner, best_player))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_tournament(id):
    cursor = create_connection()
    statement = """DELETE FROM TOURNAMENTS WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_tournament(nameFind, yearFind, winnerFind, best_playerFind):
    statement = """SELECT * FROM TOURNAMENTS WHERE(NAME LIKE  '{}%' ) AND (YEAR LIKE '{}%' ) AND (CAST(WINNER AS VARCHAR(20)) LIKE '{}%' )  AND (CAST(BEST_PLAYER AS VARCHAR(9)) LIKE '{}%' )""".format(nameFind, yearFind, winnerFind, best_playerFind)

    cursor = create_connection()
    cursor.execute(statement)
    tournaments = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return tournaments

def update_tournament(id, nameUpdate, yearUpdate, winnerUpdate, best_playerUpdate):
    cursor = create_connection()
    statement = """UPDATE TOURNAMENTS SET NAME = '{}', YEAR = '{}', WINNER = '{}', BEST_PLAYER = {} WHERE ID={} """.format(nameUpdate, yearUpdate, winnerUpdate, best_playerUpdate, id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def showJointTables():
    cursor = create_connection()
    statement= """ SELECT TOURNAMENTS.ID, TOURNAMENTS.NAME, YEAR, TEAMS.NATION , PLAYERS.NAME FROM TOURNAMENTS INNER JOIN PLAYERS ON PLAYERS.ID=TOURNAMENTS.BEST_PLAYER INNER JOIN TEAMS ON TEAMS.ID=TOURNAMENTS.WINNER  """
    cursor.execute(statement)
    tournaments = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)
    return tournaments

def findInJointTables(nameFind, yearFind, winnerFind, best_playerFind):
    statement= """ SELECT TOURNAMENTS.ID, TOURNAMENTS.NAME, YEAR, TEAMS.NATION , PLAYERS.NAME FROM TOURNAMENTS INNER JOIN PLAYERS ON PLAYERS.ID=TOURNAMENTS.BEST_PLAYER INNER JOIN TEAMS ON TEAMS.ID=TOURNAMENTS.WINNER WHERE(TOURNAMENTS.NAME LIKE  '{}%' ) AND (YEAR LIKE '{}%' ) AND (TEAMS.NATION LIKE '{}%' )  AND (PLAYERS.NAME LIKE '{}%' )""".format(nameFind, yearFind, winnerFind, best_playerFind)

    cursor = create_connection()
    cursor.execute(statement)
    tournaments = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return tournaments

@app.route("/tournaments/", methods=['GET', 'POST'])
def tournaments():

    #create_table()
    #allPlayers = players.get_players()
    allTeams=teams.get_teams()
    dsn = app.config['dsn']

    app.store = StoreP(dsn)
    allPlayers = app.store.getAllPlayers(dsn)

    if request.method == 'GET':
        #all_tournaments = get_tournaments() # get all tournaments
        all_tournaments = showJointTables()
        #queriedTournaments = find_tournament('?','?','?','?','?')
        queriedTournaments = findInJointTables('?','?','?','?')
    elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        year = request.form['year']
        winner = request.form['winner']
        best_player = request.form['best_player']
        # ----------------------------------------------

        add_new_tournament(name, year, winner, best_player) # save to db

        #all_tournaments = get_tournaments() # get all tournaments
        all_tournaments = showJointTables()
        #queriedTournaments = find_tournament('?','?','?','?','?')
        queriedTournaments = findInJointTables('?','?','?','?')
    elif 'delete' in request.form:
        ids = request.form.getlist('tournaments_to_delete')
        for id in ids:
            delete_tournament(id)
        #all_tournaments = get_tournaments()
        all_tournaments = showJointTables()
        #queriedTournaments = find_tournament('?','?','?','?','?')
        queriedTournaments = findInJointTables('?','?','?','?')
    elif 'find' in request.form:
        nameFind = request.form['nameFind']
        yearFind = request.form['yearFind']
        winnerFind = request.form['winnerFind']
        best_playerFind = request.form['best_playerFind']

        #all_tournaments = get_tournaments()
        all_tournaments = showJointTables()
        #queriedTournaments = find_tournament(nameFind,yearFind,winnerFind,second_placeFind,best_playerFind)
        queriedTournaments = findInJointTables(nameFind,yearFind,winnerFind,best_playerFind)
    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            nameUpdate = request.form['nameUpdate'+id]
            yearUpdate = request.form['yearUpdate'+id]
            winnerUpdate = request.form['winnerUpdate'+id]
            best_playerUpdate = request.form['best_playerUpdate'+id]
            update_tournament(id, nameUpdate, yearUpdate, winnerUpdate, best_playerUpdate)

        #all_tournaments = get_tournaments()
        all_tournaments = showJointTables()
        queriedTournaments = findInJointTables('?','?','?','?')
        #queriedTournaments = find_tournament('?','?','?','?','?')
    return render_template("tournaments.html", tournaments=all_tournaments, tournamentsToShow=queriedTournaments, PlayersSelect=allPlayers, TeamsSelect=allTeams)
