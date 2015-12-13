from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from team import team
from store import StoreTeam
import psycopg2 as dbapi2





@app.route('/teams', methods = ['GET', 'POST'])
def teams():

    dsn = app.config['dsn']

    app.store = StoreTeam(dsn)


    if request.method == 'GET':
        allTeams = app.store.getAllTeams(dsn)

    elif 'delete' in request.form:
        ids = request.form.getlist('teams')
        for id in ids:
            app.store.deleteTeam(id, dsn)
        allTeams = app.store.getAllTeams(dsn)


    elif 'add' in request.form:
        nation = request.form['nationToAdd']
        gender = request.form['genderToAdd']
        foundDate = request.form['foundDateToAdd']
        timesWon = request.form['timesWonToAdd']
        newTeam = team(nation, gender, foundDate, timesWon)
        app.store.addTeam(newTeam, dsn)
        allTeams = app.store.getAllTeams(dsn)

    elif 'update' in request.form:
        ids = request.form.getlist('teams')
        id = ids[0]
        nation = request.form['nationToUpdate']
        gender = request.form['genderToUpdate']
        foundDate = request.form['foundDateToUpdate']
        timesWon = request.form['timesWonToUpdate']
        updatedTeam = team(nation, gender, foundDate, timesWon)
        app.store.updateTeam(updatedTeam, id, dsn)
        allTeams = app.store.getAllTeams(dsn)

    elif 'find' in request.form:
        nation = request.form['nationToFind']
        gender = request.form['genderToFind']
        foundDate = request.form['foundDateToFind']
        timesWon = request.form['timesWonToFind']
        findTeam = team(nation, gender, foundDate, timesWon)
        allTeams = app.store.selectTeams(findTeam, dsn)


    return render_template('teams.html', teams = allTeams)



