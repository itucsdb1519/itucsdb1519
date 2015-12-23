# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2
import players
from store import StoreP


def create_table():
    cursor = create_connection()
    try:
        statement = """ CREATE TABLE PLAYERSTATISTICS(
        ID SERIAL PRIMARY KEY,
        matches_played VARCHAR(10),
        matches_won VARCHAR(10),
        win_rate VARCHAR(10),
        average_score  VARCHAR(10),
        player INTEGER REFERENCES players ON DELETE CASCADE ON UPDATE CASCADE
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        close_connection(cursor)

def create_init_playerstatistics():
    add_new_playerstatistic(2, 3, 2.3, 1.4, 1)
    add_new_playerstatistic(4, 2, 3.7, 1.7, 2)
    add_new_playerstatistic(2, 3, 2.3, 1.2, 3)


def get_playerstatistics():
    cursor = create_connection()

    cursor.execute("SELECT * FROM playerstatistics;")
    playerstatistics = cursor.fetchall()

    close_connection(cursor)

    return playerstatistics

def update_playerstatistic(id, matches_played_update, matches_won_update, win_rate_update, average_score_update, player_update):
    cursor = create_connection()
    statement = """UPDATE playerstatistics SET matches_played = '{}', matches_won = '{}', win_rate = '{}', average_score = '{}', player = '{}' WHERE ID = {}""".format( matches_played_update, matches_won_update, win_rate_update, average_score_update, player_update, id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_playerstatistic(matches_played_find, matches_won_find, win_rate_find, average_score_find, player_find):
    statement= """ SELECT playerstatistics.ID, matches_played, matches_won, win_rate, average_score, player FROM playerstatistics INNER JOIN players ON players.ID=playerstatistics.player WHERE(matches_played LIKE  '{}%' ) AND (matches_won LIKE '{}%' ) AND (win_rate LIKE '{}%' ) AND (average_score LIKE '{}%' ) AND (players.NAME LIKE '{}%' )""".format(matches_played_find, matches_won_find, win_rate_find, average_score_find, player_find)

    cursor = create_connection()
    cursor.execute(statement)
    playerstatistics = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return playerstatistics

def add_new_playerstatistic(matches_played, matches_won, win_rate, average_score, player):
    cursor = create_connection()

    cursor.execute("INSERT INTO playerstatistics (matches_played, matches_won, win_rate, average_score, player) VALUES (%s, %s, %s, %s, %s)", (matches_played, matches_won, win_rate, average_score, player))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_playerstatistic(id):
    cursor = create_connection()
    statement = """DELETE FROM playerstatistics WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def join_tables():
    cursor = create_connection()
    statement= """ SELECT playerstatistics.ID, matches_played, matches_won, win_rate, average_score, players.NAME FROM playerstatistics INNER JOIN players ON players.ID=playerstatistics.player """
    cursor.execute(statement)
    playerstatistics = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)
    return playerstatistics


@app.route("/playerstatistics/", methods=['GET', 'POST'])
def playerstatistics():

    dsn = app.config['dsn']

    app.store = StoreP(dsn)
    all_players = app.store.getAllPlayers(dsn)

    if request.method == 'GET':
        all_playerstatistics = join_tables()

    elif 'add' in request.form:
        # ----------------------------------------------
        matches_played = request.form['matches_played']
        matches_won = request.form['matches_won']
        win_rate = request.form['win_rate']
        average_score = request.form['average_score']
        player = request.form['player']
        # ----------------------------------------------

        add_new_playerstatistic(matches_played, matches_won, win_rate, average_score, player) # save to db

        all_playerstatistics = join_tables()

    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            matches_played_update = request.form['matches_played_update'+id]
            matches_won_update = request.form['matches_won_update'+id]
            win_rate_update = request.form['win_rate_update'+id]
            average_score_update = request.form['average_score_update'+id]
            player_update = request.form['player_update'+id]

            update_playerstatistic(id,matches_played_update,matches_won_update,win_rate_update,average_score_update,player_update)

        all_playerstatistics = join_tables()

    elif 'find' in request.form:
        matches_played = request.form['matches_played_find']
        matches_won = request.form['matches_won_find']
        win_rate = request.form['win_rate_find']
        average_score = request.form['average_score_find']
        player = request.form['player_find']

        all_playerstatistics= find_playerstatistic(matches_played,matches_won,win_rate,average_score,player)

    elif 'delete' in request.form:
        ids = request.form.getlist('playerstatistics_to_delete')
        for id in ids:
            delete_playerstatistic(id)

        all_playerstatistics = join_tables()

    elif 'showall' in request.form:

        all_playerstatistics = join_tables()

    return render_template("playerstatistics.html", playerstatistics=all_playerstatistics, players_select=all_players)
