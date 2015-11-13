from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config import app
from technicmember import tm
from store import Store
import psycopg2 as dbapi2






@app.route('/technicMembers', methods = ['GET', 'POST'])
def technicMembers():

    dsn = """user=vagrant password=vagrant
    host=localhost port=54321 dbname=itucsdb"""

    app.store = Store(dsn)
    app.store.createTable(dsn)

    if request.method == 'GET':
        allTms = app.store.getAllTms(dsn)

    elif 'delete' in request.form:
        ids = request.form.getlist('tms_to_delete')
        for id in ids:
            app.store.deleteTm(dsn,id)
        allTms = app.store.getAllTms(dsn)


    elif 'add' in request.form:
        name = request.form['name']
        gender = request.form['gender']
        newTm = tm(name, gender)
        app.store.addTm(dsn, newTm)
        allTms = app.store.getAllTms(dsn)

    return render_template('technicMembers.html', tms = allTms )



