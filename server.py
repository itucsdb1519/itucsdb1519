import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/coaches')
def coaches():
    now = datetime.datetime.now()
    return render_template('coaches.html', current_time=now.ctime())

@app.route('/players')
def movies_page():
    return render_template('players.html')


if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
    app.run(host='0.0.0.0', port=int(PORT))
