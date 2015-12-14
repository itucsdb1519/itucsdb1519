# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2
import teams
from store import StoreTeam


def create_table():
    cursor = create_connection()
    try:
        statement = """ CREATE TABLE COACHES(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        GENDER VARCHAR(6),
        NATIONALITY VARCHAR(45),
        BIRTH_DATE  VARCHAR(10),
        CURRENT_TEAM INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        close_connection(cursor)


def get_coaches():
    cursor = create_connection()

    cursor.execute("SELECT * FROM coaches;")
    coaches = cursor.fetchall()

    close_connection(cursor)

    return coaches

def create_init_coaches():

    add_new_coach('Zehra', 'female', 'turkish', '1964', 1)
    add_new_coach('Mike', 'male', 'english', '1954', 2)
    add_new_coach('Chan', 'male', 'chinese', '1962', 3)


def update_coach(id, name_update, gender_update, nationality_update, birth_date_update, current_team_update):
    cursor = create_connection()
    statement = """UPDATE COACHES SET NAME = '{}', GENDER = '{}', NATIONALITY = '{}', BIRTH_DATE = '{}', CURRENT_TEAM = '{}' WHERE ID = {}""".format(name_update, gender_update, nationality_update, birth_date_update, current_team_update,id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_coach(name_find, gender_find, nationality_find, birth_date_find, current_team_find):
    statement= """ SELECT COACHES.ID, COACHES.NAME, COACHES.GENDER, NATIONALITY, BIRTH_DATE, TEAMS.NATION FROM COACHES INNER JOIN TEAMS ON TEAMS.ID=COACHES.CURRENT_TEAM WHERE(COACHES.NAME LIKE  '{}%' ) AND (COACHES.GENDER LIKE '{}%' ) AND (NATIONALITY LIKE '{}%' ) AND (BIRTH_DATE LIKE '{}%' ) AND (TEAMS.NATION LIKE '{}%' )""".format(name_find, gender_find, nationality_find, birth_date_find, current_team_find)

    cursor = create_connection()
    cursor.execute(statement)
    coaches = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return coaches

def add_new_coach(name, gender, nationality, birth_date, current_team):
    cursor = create_connection()

    cursor.execute("INSERT INTO coaches (name, gender, nationality, birth_date, current_team) VALUES (%s, %s, %s, %s, %s)", (name, gender, nationality, birth_date, current_team))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_coach(id):
    cursor = create_connection()
    statement = """DELETE FROM COACHES WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def join_tables():
    cursor = create_connection()
    statement= """ SELECT COACHES.ID, COACHES.NAME, COACHES.GENDER, NATIONALITY, BIRTH_DATE, TEAMS.NATION FROM COACHES INNER JOIN TEAMS ON TEAMS.ID=COACHES.CURRENT_TEAM  """
    cursor.execute(statement)
    coaches = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)
    return coaches


@app.route("/coaches/", methods=['GET', 'POST'])
def coaches():
    dsn = app.config['dsn']

    app.store = StoreTeam(dsn)
    all_teams = app.store.getAllTeams(dsn)

    if request.method == 'GET':
        all_coaches = join_tables()

    elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        gender = request.form['gender']
        nationality = request.form['nationality']
        birth_date = request.form['birth_date']
        current_team = request.form['current_team']
        # ----------------------------------------------

        add_new_coach(name, gender, nationality, birth_date, current_team) # save to db

        all_coaches = join_tables()

    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            name_update = request.form['name_update'+id]
            gender_update = request.form['gender_update'+id]
            nationality_update = request.form['nationality_update'+id]
            birth_date_update = request.form['birth_date_update'+id]
            current_team_update = request.form['current_team_update'+id]

            update_coach(id,name_update,gender_update,nationality_update,birth_date_update,current_team_update)

        all_coaches = join_tables()

    elif 'find' in request.form:
        para_1 = request.form['name_find']
        para_2 = request.form['gender_find']
        para_3 = request.form['nationality_find']
        para_4 = request.form['birth_date_find']
        para_5 = request.form['current_team_find']

        all_coaches = find_coach(para_1,para_2,para_3,para_4,para_5)

    elif 'delete' in request.form:
        ids = request.form.getlist('coaches_to_delete')
        for id in ids:
            delete_coach(id)

        all_coaches = join_tables()

    elif 'showall' in request.form:

        all_coaches = join_tables()

    return render_template("coaches.html", coaches=all_coaches, teams_select=all_teams)
