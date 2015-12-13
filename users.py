# -*- coding: utf-8 -*-
from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2


def create_table():
    cursor = create_connection()
    try:
        statement = """ CREATE TABLE USERS(
        ID SERIAL PRIMARY KEY,
        USERNAME VARCHAR(45),
        PASSWORD VARCHAR(6)
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        close_connection(cursor)


def get_users():
    cursor = create_connection()

    cursor.execute("SELECT * FROM USERS;")
    users = cursor.fetchall()

    close_connection(cursor)

    return users

def update_user(id, username_update, password_update):
    cursor = create_connection()
    statement = """UPDATE USERS SET USERNAME = '{}', PASSWORD = '{}' WHERE ID = {}""".format(username_update, password_update,id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_user(para_1, para_2):

    statement = """SELECT * FROM USERS WHERE(USERNAME LIKE  '{}%' ) AND (PASSWORD LIKE '{}%' )""".format(para_1,para_2)

    cursor = create_connection()
    cursor.execute(statement)
    users = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return users

def add_new_user(username, password):
    cursor = create_connection()

    cursor.execute("INSERT INTO USERS (USERNAME, PASSWORD) VALUES (%s, %s)", (username, password))
    cursor.connection.commit()

    close_connection(cursor)

    return True


def delete_user(id):
    cursor = create_connection()
    statement = """DELETE FROM USERS WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)


@app.route("/users/", methods=['GET', 'POST'])
def USERS():

    #create_table()

    if request.method == 'GET':
        all_users = get_users() # get all USERS

    elif 'add' in request.form:
        # ----------------------------------------------
        username = request.form['username']
        password = request.form['password']
        # ----------------------------------------------

        add_new_user(username, password) # save to db

        all_users = get_users() # get all USERS

    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            username_update = request.form['username_update'+id]
            password_update = request.form['password_update'+id]

            update_user(id,username_update,password_update)
        all_users = get_users()

    elif 'find' in request.form:
        para_1 = request.form['username_find']
        para_2 = request.form['password_find']

        all_users = find_user(para_1,para_2)


    elif 'delete' in request.form:
        ids = request.form.getlist('users_to_delete')
        for id in ids:
            delete_user(id)
        all_users = get_users()

    elif 'showall' in request.form:
        all_users = get_users()

    return render_template("users.html", users=all_users)
