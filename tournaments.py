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

@app.route("/tournaments/", methods=['GET', 'POST'])
def tournaments():

    #create_table()

    if request.method == 'GET':
        all_tournaments = get_tournaments() # get all tournaments

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
    elif 'delete' in request.form:
        ids = request.form.getlist('tournaments_to_delete')
        for id in ids:
            delete_tournament(id)
        all_tournaments = get_tournaments()
    return render_template("tournaments.html", tournaments=all_tournaments)
