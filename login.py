from flask import request

from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2

def create_table():
    cursor = create_connection()
    try:
        statement = """ CREATE TABLE users(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45) NOT NULL UNIQUE,
        PASSWORD VARCHAR(45) NOT NULL
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        close_connection(cursor)


def get_users():
    cursor = create_connection()

    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()

    close_connection(cursor)

    return users


def add_new_user(name, password):
    cursor = create_connection()

    cursor.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (name, password))
    cursor.connection.commit()

    close_connection(cursor)

    return True


def delete_user(id):
    cursor = create_connection()
    statement = """DELETE FROM users WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)


@app.route("/login", methods=['GET', 'POST'])
def users():

    create_table()

    if request.method == 'GET':
        all_users = get_users() # get all users

    elif 'SignUp' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        password = request.form['password']
        # ----------------------------------------------

        add_new_user(name, password) # save to db

        all_users = get_users() # get all users
    elif 'delete' in request.form:
        ids = request.form.getlist('users_to_delete')
        for id in ids:
            delete_user(id)
        all_users = get_users()
    return render_template("login.html", users=all_users)
