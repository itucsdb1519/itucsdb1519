from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2



def create_table():
    try:
        cursor = create_connection()
        statement = """ CREATE TABLE PLAYERS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        GENDER VARCHAR(6),
        NATIONALITY VARCHAR(45),
        BIRTH_DATE  DATE,
        CURRENT_TEAM VARCHAR(20),
        TIMES_WON VARCHAR(10)
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
        close_connection(cursor)
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        cursor.connection.close()

def get_players():
    cursor = create_connection()

    cursor.execute("SELECT * FROM PLAYERS;")
    players = cursor.fetchall()

    close_connection(cursor)

    return players


def add_new_player(name, gender, nationality, birth_date, current_team, times_won):
    cursor = create_connection()

    cursor.execute("INSERT INTO PLAYERS (NAME, GENDER, NATIONALITY, BIRTH_DATE, CURRENT_TEAM, TIMES_WON) VALUES (%s, %s, %s, %s, %s, %s)", (name, gender, nationality, birth_date, current_team, times_won))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_player(id):
    cursor = create_connection()
    statement = """DELETE FROM PLAYERS WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

@app.route("/players", methods=['GET', 'POST'])
def players():

    create_table()

    if request.method == 'GET':
        all_players = get_players() # get all players

    elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        gender = request.form['gender']
        nationality = request.form['nationality']
        birth_date = request.form['birth_date']
        current_team = request.form['current_team']
        times_won = request.form['times_won']
        # ----------------------------------------------

        add_new_player(name, gender, nationality, birth_date, current_team, times_won) # save to db

        all_players = get_players() # get all players
    elif 'delete' in request.form:
        ids = request.form.getlist('players_to_delete')
        for id in ids:
            delete_player(id)
        all_players = get_players()

    return render_template("players.html", players=all_players)