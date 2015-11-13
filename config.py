from flask import Flask

app = Flask(__name__)

app.debug = True


import psycopg2


# database settings -----------------------------------
DB_SETTINGS = {
    'database': "itucsdb",
    'user': "vagrant",
    'password': "vagrant",
    'host': "localhost",
    'port': "54321",
}

# Database connections



def create_connection():
    connection = psycopg2.connect(**DB_SETTINGS)
    cursor = connection.cursor()
    return cursor


def close_connection(cursor):
    connection = cursor.connection
    cursor.close()
    connection.close()
    return True
# -----------------------------------------------------
