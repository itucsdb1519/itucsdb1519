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
        statement = """ CREATE TABLE STADIUMS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        CAPACITY VARCHAR(45),
        CITY VARCHAR(45),
        COUNTRY INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        close_connection(cursor)

def create_init_stadiums():

    add_new_stadium('Marmara', '20000', 'Istanbul', 1)
    add_new_stadium('Wembley', '30000', 'London', 2)
    add_new_stadium('Moscow', '25000', 'St.Petersburg', 4)



def get_stadiums():
    cursor = create_connection()

    cursor.execute("SELECT * FROM stadiums;")
    stadiums = cursor.fetchall()

    close_connection(cursor)

    return stadiums

def update_stadium(id, name_update, capacity_update, city_update, country_update ):
    cursor = create_connection()
    statement = """UPDATE STADIUMS SET NAME = '{}', CAPACITY = '{}', CITY = '{}', COUNTRY = '{}'  WHERE ID = {}""".format(name_update, capacity_update, city_update, country_update, id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def find_stadium(name_find, capacity_find, city_find, country_find ):
    statement= """ SELECT STADIUMS.ID, STADIUMS.NAME, STADIUMS.CAPACITY, CITY, TEAMS.NATION FROM STADIUMS INNER JOIN TEAMS ON TEAMS.ID=STADIUMS.COUNTRY WHERE(STADIUMS.NAME LIKE  '{}%' ) AND (STADIUMS.CAPACITY LIKE '{}%' ) AND (CITY LIKE '{}%' ) AND (TEAMS.NATION LIKE '{}%' )""".format(name_find, capacity_find, city_find, country_find)

    cursor = create_connection()
    cursor.execute(statement)
    stadiums = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return stadiums

def add_new_stadium(name, capacity, city, country):
    cursor = create_connection()

    cursor.execute("INSERT INTO stadiums (name, capacity, city, country) VALUES (%s, %s, %s, %s)", (name, capacity, city, country))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_stadium(id):
    cursor = create_connection()
    statement = """DELETE FROM STADIUMS WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

def join_tables():
    cursor = create_connection()
    statement= """ SELECT STADIUMS.ID, STADIUMS.NAME, STADIUMS.CAPACITY, CITY, TEAMS.NATION FROM STADIUMS INNER JOIN TEAMS ON TEAMS.ID=STADIUMS.COUNTRY  """
    cursor.execute(statement)
    stadiums = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)
    return stadiums


@app.route("/stadiums/", methods=['GET', 'POST'])
def stadiums():
    dsn = app.config['dsn']

    app.store = StoreTeam(dsn)
    all_teams = app.store.getAllTeams(dsn)

    if request.method == 'GET':
        all_stadiums = join_tables()

    elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        capacity = request.form['capacity']
        city = request.form['city']
        country= request.form['country']
        # ----------------------------------------------

        add_new_stadium(name, capacity, city, country) # save to db

        all_stadiums = join_tables()

    elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            name_update = request.form['name_update'+id]
            capacity_update = request.form['capacity_update'+id]
            city_update = request.form['city_update'+id]
            country_update = request.form['country_update'+id]

            update_stadium(id,name_update,capacity_update,city_update,country_update)

        all_stadiums = join_tables()

    elif 'find' in request.form:
        para_1 = request.form['name_find']
        para_2 = request.form['capacity_find']
        para_3 = request.form['city_find']
        para_4 = request.form['country_find']


        all_stadiums = find_stadium(para_1,para_2,para_3,para_4)

    elif 'delete' in request.form:
        ids = request.form.getlist('stadiums_to_delete')
        for id in ids:
            delete_stadium(id)

        all_stadiums = join_tables()

    elif 'showall' in request.form:

        all_stadiums = join_tables()

    return render_template("stadiums.html",stadiums=all_stadiums, teams_select=all_teams)
