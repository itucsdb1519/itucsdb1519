# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2



def create_table():
    try:
        cursor = create_connection()
        statement = """ CREATE TABLE REFEREES(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        GENDER VARCHAR(6),
        NATIONALITY VARCHAR(45),
        BIRTH_DATE  VARCHAR(20),
        TIMES_MATCH VARCHAR(20)
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
        close_connection(cursor)
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        cursor.connection.close()

def get_referees():
    cursor = create_connection()

    cursor.execute("SELECT * FROM referees;")
    referees = cursor.fetchall()

    close_connection(cursor)

    return referees


def add_new_referee(name, gender, nationality, birth_date, times_match):
    cursor = create_connection()

    cursor.execute("INSERT INTO referees (name, gender, nationality, birth_date, times_match) VALUES (%s, %s, %s, %s, %s)", (name, gender, nationality, birth_date, times_match))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_referee(id):
    cursor = create_connection()
    statement = """DELETE FROM REFEREES WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

@app.route("/referees/", methods=['GET', 'POST'])
def referees():

    #create_table()

    if request.method == 'GET':
        all_referees = get_referees()

    elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        gender = request.form['gender']
        nationality = request.form['nationality']
        birth_date = request.form['birth_date']
        times_match= request.form['times_match']
        # ----------------------------------------------

        add_new_referee(name, gender, nationality, birth_date, times_match) # save to db

        all_referees = get_referees()
    elif 'delete' in request.form:
        ids = request.form.getlist('referees_to_delete')
        for id in ids:
            delete_referee(id)
        all_referees = get_referees()
    return render_template("referees.html", referees=all_referees)
