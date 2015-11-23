# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2


def create_table():
    cursor = create_connection()
    try:
        statement = """ CREATE TABLE COACHES(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        GENDER VARCHAR(6),
        NATIONALITY VARCHAR(45),
        BIRTH_DATE  VARCHAR(10),
        CURRENT_TEAM VARCHAR(20)
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

def update_coach(id, name_update, gender_update, nationality_update, birth_date_update, current_team_update):
    cursor = create_connection()
    statement = """UPDATE COACHES SET NAME = '{}', GENDER = '{}', NATIONALITY = '{}', BIRTH_DATE = '{}', CURRENT_TEAM = '{}' WHERE ID = {}""".format(name_update, gender_update, nationality_update, birth_date_update, current_team_update,id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_coach(para_1, para_2, para_3, para_4, para_5):

    statement = """SELECT * FROM COACHES WHERE(NAME LIKE  '{}%' ) AND (GENDER LIKE '{}%' ) AND (NATIONALITY LIKE '{}%' ) AND (BIRTH_DATE LIKE '{}%' ) AND (CURRENT_TEAM LIKE '{}%' )""".format(para_1,para_2,para_3,para_4,para_5)

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


@app.route("/coaches/", methods=['GET', 'POST'])
def coaches():

    #create_table()

    if request.method == 'GET':
        all_coaches = get_coaches() # get all coaches

    elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        gender = request.form['gender']
        nationality = request.form['nationality']
        birth_date = request.form['birth_date']
        current_team = request.form['current_team']
        # ----------------------------------------------

        add_new_coach(name, gender, nationality, birth_date, current_team) # save to db

        all_coaches = get_coaches() # get all coaches

    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            name_update = request.form['name_update'+id]
            gender_update = request.form['gender_update'+id]
            nationality_update = request.form['nationality_update'+id]
            birth_date_update = request.form['birth_date_update'+id]
            current_team_update = request.form['current_team_update'+id]

            update_coach(id,name_update,gender_update,nationality_update,birth_date_update,current_team_update)
        all_coaches = get_coaches()

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
        all_coaches = get_coaches()
    elif 'showall' in request.form:
        all_coaches = get_coaches()
    return render_template("coaches.html", coaches=all_coaches)
