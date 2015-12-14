# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
from store import StoreTeam
import psycopg2
import referees
import teams


def create_table():
    cursor = create_connection()
    try:
        statement = """ CREATE TABLE MATCHSTATISTICS(
        ID SERIAL PRIMARY KEY,
        HOME_TEAM INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
        AWAY_TEAM INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
        MATCH_DATE VARCHAR(45),
        SCORE  VARCHAR(10),
        REFEREE INTEGER REFERENCES REFEREES ON DELETE CASCADE ON UPDATE CASCADE
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        close_connection(cursor)


def get_matchstatistics():
    cursor = create_connection()

    cursor.execute("SELECT * FROM matchstatistics;")
    matchstatistics = cursor.fetchall()

    close_connection(cursor)

    return matchstatistics

def update_matchstatistic(id, home_team_update, away_team_update, match_date_update, score_update, referee_update):
    cursor = create_connection()
    statement = """UPDATE MATCHSTATISTICS SET HOME_TEAM = '{}', AWAY_TEAM = '{}', MATCH_DATE = '{}', SCORE = '{}', REFEREE = '{}' WHERE ID = {}""".format( home_team_update, away_team_update, match_date_update, score_update, referee_update, id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_matchstatistic(home_team_find, away_team_find, match_date_find, score_find, referee_find):
    statement= """ SELECT MATCHSTATISTICS.ID, t1.NATION, t2.NATION, MATCH_DATE, SCORE, REFEREES.NAME FROM MATCHSTATISTICS INNER JOIN REFEREES ON REFEREES.ID=MATCHSTATISTICS.REFEREE INNER JOIN TEAMS t1 ON t1.ID=MATCHSTATISTICS.HOME_TEAM INNER JOIN TEAMS t2 ON t2.ID=MATCHSTATISTICS.AWAY_TEAM  WHERE(t1.NATION LIKE  '{}%' ) AND (t2.NATION LIKE '{}%' ) AND (MATCH_DATE LIKE '{}%' ) AND (SCORE LIKE '{}%' ) AND (REFEREES.NAME LIKE '{}%' )""".format(home_team_find, away_team_find, match_date_find, score_find, referee_find)

    cursor = create_connection()
    cursor.execute(statement)
    matchstatistics = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return matchstatistics

def add_new_matchstatistic(home_team, away_team, match_date, score, referee):
    cursor = create_connection()

    cursor.execute("INSERT INTO matchstatistics (home_team, away_team, match_date, score, referee) VALUES (%s, %s, %s, %s, %s)", (home_team, away_team, match_date, score, referee))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_matchstatistic(id):
    cursor = create_connection()
    statement = """DELETE FROM MATCHSTATISTICS WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def join_tables():
    cursor = create_connection()
    statement= """ SELECT MATCHSTATISTICS.ID, t1.NATION, t2.NATION, MATCH_DATE, SCORE, REFEREES.NAME FROM MATCHSTATISTICS INNER JOIN REFEREES ON REFEREES.ID=MATCHSTATISTICS.REFEREE INNER JOIN TEAMS t1 ON t1.ID=MATCHSTATISTICS.HOME_TEAM INNER JOIN TEAMS t2 ON t2.ID=MATCHSTATISTICS.AWAY_TEAM"""
    cursor.execute(statement)
    matchstatistics = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)
    return matchstatistics


@app.route("/matchstatistics/", methods=['GET', 'POST'])
def matchstatistics():

    all_referees = referees.get_referees()
    dsn = app.config['dsn']

    app.storeT = StoreTeam(dsn)
    allTeams = app.storeT.getAllTeams(dsn)

    if request.method == 'GET':
        all_matchstatistics = join_tables()

    elif 'add' in request.form:
        # ----------------------------------------------
        home_team = request.form['home_team']
        away_team = request.form['away_team']
        match_date = request.form['match_date']
        score = request.form['score']
        referee = request.form['referee']
        # ----------------------------------------------

        add_new_matchstatistic(home_team, away_team, match_date, score, referee) # save to db

        all_matchstatistics = join_tables()

    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            home_team_update = request.form['home_team_update'+id]
            away_team_update = request.form['away_team_update'+id]
            match_date_update = request.form['match_date_update'+id]
            score_update = request.form['score_update'+id]
            referee_update = request.form['referee_update'+id]

            update_matchstatistic(id,home_team_update,away_team_update,match_date_update,score_update,referee_update)

        all_matchstatistics = join_tables()

    elif 'find' in request.form:
        home_team = request.form['home_team_find']
        away_team = request.form['away_team_find']
        match_date = request.form['match_date_find']
        score = request.form['score_find']
        referee = request.form['referee_find']

        all_matchstatistics= find_matchstatistic(home_team,away_team,match_date,score,referee)

    elif 'delete' in request.form:
        ids = request.form.getlist('matchstatistics_to_delete')
        for id in ids:
            delete_matchstatistic(id)

        all_matchstatistics = join_tables()

    elif 'showall' in request.form:

        all_matchstatistics = join_tables()

    return render_template("matchstatistics.html", matchstatistics=all_matchstatistics, referees_select=all_referees, TeamsSelect=allTeams)
