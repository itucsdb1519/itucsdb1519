from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from technicmember import tm
from store import StoreTM
import psycopg2 as dbapi2





@app.route('/technicMembers', methods = ['GET', 'POST'])
def technicMembers():

    dsn = app.config['dsn']

    app.store = StoreTM(dsn)

    if request.method == 'GET':
        allTms = app.store.getAllTms(dsn)

    elif 'delete' in request.form:
        ids = request.form.getlist('tms')
        for id in ids:
            app.store.deleteTm(id, dsn)
        allTms = app.store.getAllTms(dsn)


    elif 'add' in request.form:
        name = request.form['nameToAdd']
        gender = request.form['genderToAdd']
        newTm = tm(name, gender)
        app.store.addTm(newTm, dsn)
        allTms = app.store.getAllTms(dsn)

    elif 'update' in request.form:
        ids = request.form.getlist('tms')
        id = ids[0]
        name = request.form['nameToUpdate']
        gender = request.form['genderToUpdate']
        newTm = tm(name, gender)
        app.store.updateTm(newTm, id, dsn)
        allTms = app.store.getAllTms(dsn)

    elif 'find' in request.form:
        name = request.form['nameToFind']
        gender = request.form['genderToFind']
        findTm = tm(name, gender)
        allTms = app.store.selectTms(findTm, dsn)


    return render_template('technicMembers.html', tms = allTms )






