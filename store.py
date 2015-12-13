import psycopg2 as dbapi2

from technicmember import tm
from player import player

import teams



class StoreTM:
    def __init__(self, dbSettings):
        self.dsn = dbSettings

    def createTable(self, dsn):
        try:
            connection = dbapi2.connect(dsn)
            cursor = connection.cursor()
            statement = """ CREATE TABLE TECHNICMEMBERS (
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(45),
            GENDER VARCHAR(6)
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            connection.close()

    def addTm(self, tm, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO TECHNICMEMBERS (NAME, GENDER) VALUES(%s, %s)", (tm.name, tm.gender))

    def updateTm(self, tm, id, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """UPDATE TECHNICMEMBERS SET NAME= '{}', GENDER = '{}' WHERE ID = {} """.format(tm.name, tm.gender, id)
                cursor.execute(query)

    def deleteTm(self, id, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ DELETE FROM TECHNICMEMBERS WHERE ID = {}""".format(id)
                cursor.execute(query)

    def selectTms(self, tm, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """SELECT * FROM TECHNICMEMBERS WHERE(NAME LIKE  '{}%' ) AND (GENDER LIKE '{}%' )""".format(tm.name, tm.gender)
                cursor.execute(query)
                tms = cursor.fetchall()
                return tms

    def getAllTms (self, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ SELECT * FROM TECHNICMEMBERS """
                cursor.execute(query)
                tms = cursor.fetchall()
                return tms

class StoreP:
    def __init__(self, dbSettings):
        self.dsn = dbSettings

    def createTable(self, dsn):
        try:
            connection = dbapi2.connect(dsn)
            cursor = connection.cursor()
            statement = """ CREATE TABLE PLAYERS (
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(45),
            GENDER VARCHAR(6),
            NATION VARCHAR(45),
            BIRTHDATE VARCHAR(10),
            TEAM INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            connection.close()

    def addPlayer(self, player, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO PLAYERS (NAME, GENDER, NATION, BIRTHDATE, TEAM) VALUES(%s, %s, %s, %s, %s)", (player.name, player.gender, player.nation, player.birthDate, player.team))

    def updatePlayer(self, player, id, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """UPDATE PLAYERS SET NAME = '{}', GENDER = '{}', NATION = '{}', BIRTHDATE = '{}', TEAM = '{}' WHERE ID = {} """.format(player.name, player.gender, player.nation, player.birthDate, player.team, id)
                cursor.execute(query)

    def deletePlayer(self, id, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ DELETE FROM PLAYERS WHERE ID = {}""".format(id)
                cursor.execute(query)

    def selectPlayers(self, player, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """SELECT PLAYERS.ID, PLAYERS.NAME, PLAYERS.GENDER, PLAYERS.NATION, PLAYERS.BIRTHDATE, TEAMS.NATION
                FROM PLAYERS INNER JOIN TEAMS ON TEAMS.ID = PLAYERS.TEAM
                WHERE(PLAYERS.NAME LIKE  '{}%' ) AND (PLAYERS.GENDER LIKE '{}%' ) AND
                (PLAYERS.NATION LIKE '{}%' ) AND (PLAYERS.BIRTHDATE LIKE '{}%' ) AND
                (TEAMS.NATION LIKE '{}%' ) """.format(player.name, player.gender, player.nation, player.birthDate, player.team)
                cursor.execute(query)
                players = cursor.fetchall()
                return players

    def getAllPlayers (self, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ SELECT PLAYERS.ID, PLAYERS.NAME, PLAYERS.GENDER, PLAYERS.NATION, PLAYERS.BIRTHDATE, TEAMS.NATION FROM PLAYERS INNER JOIN TEAMS ON TEAMS.ID = PLAYERS.TEAM """
                cursor.execute(query)
                players = cursor.fetchall()
                return players