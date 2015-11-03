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
        BIRTH_DATE  DATE,
        CURRENT_TEAM VARCHAR(20)
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
        close_connection(cursor)
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        cursor.connection.close()

create_table()

def get_coaches():
    cursor = create_connection()

    cursor.execute("SELECT * FROM coaches;")
    coaches = cursor.fetchall()

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
    elif 'delete' in request.form:
        ids = request.form.getlist('coaches_to_delete')
        for id in ids:
            delete_coach(id)
        all_coaches = get_coaches()
    return render_template("coaches.html", coaches=all_coaches)
