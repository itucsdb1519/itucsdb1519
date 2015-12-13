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
def update_referee(id, name_update, gender_update, nationality_update, birth_date_update, times_match_update):
    cursor = create_connection()
    statement = """UPDATE REFEREES SET NAME = '{}', GENDER = '{}', NATIONALITY = '{}', BIRTH_DATE = '{}', TIMES_MATCH = '{}' WHERE ID = {}""".format(name_update, gender_update, nationality_update, birth_date_update, times_match_update,id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_referee(d1,d2,d3,d4,d5):
    cursor = create_connection()
    statement = """SELECT * FROM referees WHERE (NAME LIKE  '{}%' ) AND (GENDER LIKE '{}%' ) AND (NATIONALITY LIKE  '{}%' ) AND (BIRTH_DATE LIKE  '{}%' ) AND (TIMES_MATCH LIKE  '{}%' )""".format(d1,d2,d3,d4,d5)


    cursor.execute(statement)
    referees = cursor.fetchall()
    cursor.connection.commit()
    close_connection(cursor)

    return referees

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

    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            name_update = request.form['name_update'+id]
            gender_update = request.form['gender_update'+id]
            nationality_update = request.form['nationality_update'+id]
            birth_date_update = request.form['birth_date_update'+id]
            times_match_update = request.form['times_match_update'+id]


            update_referee(id,name_update,gender_update,nationality_update,birth_date_update,times_match_update)
        all_referees = get_referees()

    elif 'find' in request.form:
        d1 = request.form['name_find']
        d2 = request.form['gender_find']
        d3 = request.form['nationality_find']
        d4 = request.form['birth_date_find']
        d5 = request.form['times_match_find']

        all_referees = find_referee(d1,d2,d3,d4,d5)

    elif 'showall' in request.form:
        all_referees = get_referees()

    return render_template("referees.html", referees=all_referees)