import psycopg2 as dbapi2

from technicmember import tm



class Store:
    def __init__(self, dsn):
        dsn = dsn

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

    def addTm(self, dsn, tm):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO TECHNICMEMBERS (NAME, GENDER) VALUES(%s, %s)", (tm.name, tm.gender))

    def deleteTm(self, dsn, id):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ DELETE FROM TECHNICMEMBERS WHERE ID = {}""".format(id)
                cursor.execute(query)

    def selectTm(self, dsn, id):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """SELECT FROM TECHNICMEMBERS WHERE (ID = ?)"""
                cursor.execute(query,id)
                return tm

    def getAllTms (self, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ SELECT * FROM TECHNICMEMBERS """
                cursor.execute(query)
                tms = cursor.fetchall()
                return tms