from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from player import player
from store import StoreP
import psycopg2 as dbapi2
import teams





@app.route('/players', methods = ['GET', 'POST'])
def players():

    dsn = app.config['dsn']

    app.store = StoreP(dsn)

    allTeams = teams.get_teams()

    if request.method == 'GET':
        allPlayers = app.store.getAllPlayers(dsn)

    elif 'delete' in request.form:
        ids = request.form.getlist('players')
        for id in ids:
            app.store.deletePlayer(id, dsn)
        allPlayers = app.store.getAllPlayers(dsn)


    elif 'add' in request.form:
        name = request.form['nameToAdd']
        gender = request.form['genderToAdd']
        nation = request.form['nationToAdd']
        birthDate = request.form['birthDateToAdd']
        team = request.form['teamToAdd']
        newPlayer = player(name, gender, nation, birthDate, team)
        app.store.addPlayer(newPlayer, dsn)
        allPlayers = app.store.getAllPlayers(dsn)

    elif 'update' in request.form:
        ids = request.form.getlist('players')
        id = ids[0]
        name = request.form['nameToUpdate']
        gender = request.form['genderToUpdate']
        nation = request.form['nationToUpdate']
        birthDate = request.form['birthDateToUpdate']
        team = request.form['teamToUpdate']
        updatedPlayer = player(name, gender, nation, birthDate, team)
        app.store.updatePlayer(updatedPlayer, id, dsn)
        allPlayers = app.store.getAllPlayers(dsn)

    elif 'find' in request.form:
        name = request.form['nameToFind']
        gender = request.form['genderToFind']
        nation = request.form['nationToFind']
        birthDate = request.form['birthDateToFind']
        team = request.form['teamToFind']
        findPlayer = player(name, gender, nation, birthDate, team)
        allPlayers = app.store.selectPlayers(findPlayer, dsn)


    return render_template('players.html', players = allPlayers, teams = allTeams )