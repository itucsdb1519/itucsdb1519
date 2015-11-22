# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2



def create_table():
    try:
        cursor = create_connection()
        statement = """ CREATE TABLE TOURNAMENTS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        YEAR VARCHAR(4),
        WINNER VARCHAR(45),
        SECOND_PLACE  VARCHAR(20),
        BEST_PLAYER VARCHAR(20)
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


def add_new_tournament(name, year, winner, second_place, best_player):
    cursor = create_connection()

    cursor.execute("INSERT INTO tournaments (name, year, winner, second_place, best_player) VALUES (%s, %s, %s, %s, %s)", (name, year, winner, second_place, best_player))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_tournament(id):
    cursor = create_connection()
    statement = """DELETE FROM TOURNAMENTS WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_tournament(nameFind, yearFind, winnerFind, second_placeFind, best_playerFind):
    statement = """SELECT * FROM TOURNAMENTS WHERE(NAME LIKE  '{}%' ) AND (YEAR LIKE '{}%' ) AND (WINNER LIKE '{}%' ) AND (SECOND_PLACE LIKE '{}%' ) AND (BEST_PLAYER LIKE '{}%' )""".format(nameFind, yearFind, winnerFind, second_placeFind, best_playerFind)

    cursor = create_connection()
    cursor.execute(statement)
    tournaments = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return tournaments

@app.route("/tournaments/", methods=['GET', 'POST'])
def tournaments():

    #create_table()

    if request.method == 'GET':
        all_tournaments = get_tournaments() # get all tournaments
        queriedTournaments = find_tournament('?','?','?','?','?')

    elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        year = request.form['year']
        winner = request.form['winner']
        second_place = request.form['second_place']
        best_player = request.form['best_player']
        # ----------------------------------------------

        add_new_tournament(name, year, winner, second_place, best_player) # save to db

        all_tournaments = get_tournaments() # get all tournaments
        queriedTournaments = find_tournament('?','?','?','?','?')
    elif 'delete' in request.form:
        ids = request.form.getlist('tournaments_to_delete')
        for id in ids:
            delete_tournament(id)
        all_tournaments = get_tournaments()
        queriedTournaments = find_tournament('?','?','?','?','?')
    elif 'find' in request.form:
        nameFind = request.form['nameFind']
        yearFind = request.form['yearFind']
        winnerFind = request.form['winnerFind']
        second_placeFind = request.form['second_placeFind']
        best_playerFind = request.form['best_playerFind']

        all_tournaments = get_tournaments()
        queriedTournaments = find_tournament(nameFind,yearFind,winnerFind,second_placeFind,best_playerFind)
    return render_template("tournaments.html", tournaments=all_tournaments, tournamentsToShow=queriedTournaments)
