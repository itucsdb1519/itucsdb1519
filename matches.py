# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2



def create_table():
    try:
        cursor = create_connection()
        statement = """ CREATE TABLE MATCHES(
        TOURNAMENT VARCHAR(45),
        TEAM1 VARCHAR(10),
        TEAM2 VARCHAR(20),
        WINNER  VARCHAR(20),
        DATE VARCHAR(20)
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


def add_new_match(tournament, team1, team2, winner, date):
    cursor = create_connection()

    cursor.execute("INSERT INTO matches (tournament, team1, team2, winner, date) VALUES (%s, %s, %s, %s, %s)", (tournament, team1, team2, winner, date))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_match(tournament):
    cursor = create_connection()
    statement = """DELETE FROM MATCHES WHERE TOURNAMENT='{}'""".format(tournament)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

@app.route("/matches", methods=['GET', 'POST'])
def matches():

    #create_table()

    if request.method == 'GET':
        all_matches = get_matches() # get all matches

    elif 'add' in request.form:
        # ----------------------------------------------
        tournament = request.form['tournament']
        team1 = request.form['team1']
        team2 = request.form['team2']
        winner = request.form['winner']
        date = request.form['date']
        # ----------------------------------------------

        add_new_match(tournament, team1, team2, winner, date) # save to db

        all_matches = get_matches() # get all matches
    elif 'delete' in request.form:
        tournaments = request.form.getlist('matches_to_delete')
        for tournament in tournaments:
            delete_match(tournament)
        all_matches = get_matches()
    return render_template("matches.html", matches=all_matches)
