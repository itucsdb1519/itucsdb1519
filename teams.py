# -*- coding: utf-8 -*-
from flask import request
from flask import render_template

from config import app
from config import create_connection, close_connection
import psycopg2

def create_table():
    try:
        cursor = create_connection()
        statement = """ CREATE TABLE TEAMS(
        ID SERIAL PRIMARY KEY,
        NATION VARCHAR(45),
        GENDER VARCHAR(6),
        FOUND_DATE  VARCHAR(20),
        PLAYER1_NAME VARCHAR(45),
        PLAYER2_NAME VARCHAR(45),
        TIMES_WON VARCHAR(10)
        )"""
        cursor.execute(statement)
        cursor.connection.commit()
        close_connection(cursor)
    except psycopg2.DatabaseError:
        cursor.connection.rollback()
    finally:
        cursor.connection.close()

def get_teams():
    cursor = create_connection()

    cursor.execute("SELECT * FROM TEAMS;")
    teams = cursor.fetchall()

    close_connection(cursor)

    return teams

def add_new_team(nation, gender, found_date, player1_name, player2_name, times_won):
    cursor = create_connection()

    cursor.execute("INSERT INTO TEAMS (NATION, GENDER, FOUND_DATE, PLAYER1_NAME, PLAYER2_NAME, TIMES_WON) VALUES (%s, %s, %s, %s, %s, %s)", 
            (nation, gender, found_date, player1_name, player2_name, times_won))
    cursor.connection.commit()

    close_connection(cursor)

    return True

def delete_team(id):
    cursor = create_connection()
    
    statement = """DELETE FROM TEAMS WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

@app.route("/teams/", methods=['GET', 'POST'])
def teams():
    create_table()

    if request.method == 'GET':
        all_teams = get_teams()

    elif 'add' in request.form:
        # ----------------------------------------------
        nation = request.form['nation']
        gender = request.form['gender']
        found_date = request.form['found_date']
        player1_name = request.form['player1_name']
        player2_name = request.form['player2_name']
        times_won= request.form['times_won']
        # ----------------------------------------------
        add_new_team(nation, gender, found_date, player1_name, player2_name, times_won)

        all_teams = get_teams()
        
    elif 'delete' in request.form:
        ids = request.form.getlist('teams_to_delete')
        
        for id in ids:
            delete_team(id)
            
        all_teams = get_teams()
        
    return render_template("teams.html", teams = all_teams)
