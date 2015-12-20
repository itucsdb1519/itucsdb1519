Parts Implemented by Hasan Burak NAMLI
======================================

Database Design
***************


1 Tables
--------

1.1 Teams Table
+++++++++++++++

* Teams table keeping record of the teams data


                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | ID            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |NATION         | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |GENDER         | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |FOUNDDATE      | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |TIMESWON       | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+

* *nation* keeps the record of nation of the given team.
* *gender* keeps the record of gender of the given team.
* *founddate* keeps the record of the found date of the given team.
* *timeswon* keeps the record of how many times team has won the game.


**Sql statement that initialize the teams table**:

 .. code-block:: sql

    CREATE TABLE TEAMS (
            ID SERIAL PRIMARY KEY,
            NATION VARCHAR(45),
            GENDER VARCHAR(6),
            FOUNDDATE VARCHAR(20),
            TIMESWON VARCHAR(10)
            )

1.2 Players Table
+++++++++++++++++

* Players table keeping record of the players data


                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | ID            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |NAME           | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |GENDER         | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |NATION         | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |BIRTHDATE      | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |TEAM           | INTEGER    |   0       |  0        |
                +---------------+------------+-----------+-----------+
* *name* keeps the record of name of the given player.
* *gender* keeps the record of gender of the given player.
* *nation* keeps the record of nation of the given player.
* *birthdate* keeps the record of birth date of the given player.
* *team* references to *teams* table and on delete and update operations it cascades the operation


**Sql statement that initialize the players table**:

 .. code-block:: sql

    CREATE TABLE PLAYERS (
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(45),
            GENDER VARCHAR(6),
            NATION VARCHAR(45),
            BIRTHDATE VARCHAR(10),
            TEAM INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE
            )


1.3 Technic Members Table
+++++++++++++++++++++++++

* Technic members table keeping record of the technic members data


                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | ID            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |NAME           | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |GENDER         | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |NATION         | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |BIRTHDATE      | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |COACH          | INTEGER    |   0       |  0        |
                +---------------+------------+-----------+-----------+
* *name* keeps the record of name of the given technic member.
* *gender* keeps the record of gender of the given technic member.
* *nation* keeps the record of nation of the given technic member.
* *birthdate* keeps the record of birth date of the given technic member.
* *coach* references to *coach* table and on delete and update operations it cascades the operation


**Sql statement that initialize the technic members table**:

 .. code-block:: sql

    CREATE TABLE TECHNICMEMBERS (
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(45),
            GENDER VARCHAR(6),
            NATION VARCHAR(45),
            BIRTHDATE VARCHAR(10),
            COACH INTEGER REFERENCES COACHES ON DELETE CASCADE ON UPDATE CASCADE
            )

Code
****

1 MVC and team, player,tm classes
---------------------------------

MVC pattern tried to use in the implementation of teams, players and technic members tables
in web application. For all tables classes implemented. Instances of those classes keep the
data of one tuple. Objects are implemented via html sending parameters and objects are sending
to the functions of store classes and table classes' attributes implement the database tables via store
classes' functions.

1.1 class team
++++++++++++++
* Teams table class :

   .. code-block:: python

      class team:
         def __init__(self, nation, gender, foundDate, timesWon):
            self.nation = nation
            self.gender = gender
            self.foundDate = foundDate
            self.timesWon = timesWon
1.2 class player
++++++++++++++++
* Players table class :

   .. code-block:: python

      class player:
         def __init__(self, name, gender, nation, birthDate, team):
            self.name = name
            self.gender = gender
            self.nation = nation
            self.birthDate = birthDate
            self.team = team
1.3 class tm
++++++++++++
* Technic members table class :

   .. code-block:: python

      class tm:
         def __init__(self, name, gender, nation, birthDate, coach):
            self.name = name
            self.gender = gender
            self.nation = nation
            self.birthDate = birthDate
            self.coach = coach
2 Store classes
---------------

2.1 store.py
++++++++++++

Store classes is implemented in store.py file. In store classes database is handling via some functions.
Beginning of store.py is like this:

     .. code-block:: python

      import psycopg2 as dbapi2

      from technicmember import tm
      from player import player
      from team import team

      from config import app

It imports psycopg2 editor as a dbapi2 for using as database api. Classes tm, player and team also imported.
From config.py file it imports app object. In config.py file app object implemented in this way:

     .. code-block:: python

      from flask import Flask

      app = Flask(__name__)

      app.debug = True

2.2 class StoreTeam
+++++++++++++++++++

* class StoreTeam init function and createTable function is implemented like this:

     .. code-block:: python

      class StoreTeam:
         def __init__(self, dbSettings):
            self.dsn = dbSettings

         def createTable(self, dsn):
            try:
               connection = dbapi2.connect(dsn)
               cursor = connection.cursor()
               statement = """ CREATE TABLE TEAMS (
               ID SERIAL PRIMARY KEY,
               NATION VARCHAR(45),
               GENDER VARCHAR(6),
               FOUNDDATE VARCHAR(20),
               TIMESWON VARCHAR(10)
               )"""
               cursor.execute(statement)
               connection.commit()
               cursor.close()
            except dbapi2.DatabaseError:
               connection.rollback()
            finally:
               connection.close()

createTable() function makes the connection with database via dbapi2 database api.
cursor variable created as a cursor of connection and statement variable keeps the
statement of SQL for creating table in database. After cursor execution and connection
committing try, except and finally block handles the exceptions. If any error occurs
connection rollback else connection closes.

all functions which needs to handle some operations on database uses the with .. as
context manager of psycopg2

* addTeam() function of class StoreTeam:

     .. code-block:: python

      def addTeam(self, team, dsn):
         with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO TEAMS (NATION, GENDER, FOUNDDATE, TIMESWON) VALUES(%s, %s, %s, %s)", (team.nation, team.gender, team.foundDate, team.timesWon))

This function gets a team object from teams.py file html-side function. It adds the team
object as a tuple into the database. It executes the SQL statement into the database.

* deleteTeam() function of class StoreTeam:

     .. code-block:: python

      def deleteTeam(self, id, dsn):
         with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ DELETE FROM TEAMS WHERE ID = {}""".format(id)
                cursor.execute(query)

This function gets the id of the tuple to be deleted. It deletes the tuple from the database.

* updateTeam() function of class StoreTeam:

     .. code-block:: python

      def updateTeam(self, team, id, dsn):
         with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """UPDATE TEAMS SET NATION = '{}', GENDER = '{}', FOUNDDATE = '{}', TIMESWON = '{}' WHERE ID = {} """.format(team.nation, team.gender, team.foundDate, team.timesWon, id)
                cursor.execute(query)

This function gets the id of the tuple to be updated. It reaches the tuple with its' id
and update the tuple with the team object which it gets.

* getAllTeams() function of class StoreTeam:

     .. code-block:: python

      def getAllTeams(self, dsn):
         with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ SELECT * FROM TEAMS """
                cursor.execute(query)
                teams = cursor.fetchall()
                return teams

This function select all teams and return all teams as an array.

* selectTeams() function of class StoreTeam:

     .. code-block:: python

      def selectTeams(self, team, dsn):
         with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """SELECT * FROM TEAMS WHERE(NATION LIKE  '{}%' ) AND (GENDER LIKE '{}%' ) AND (FOUNDDATE LIKE '{}%' ) AND (TIMESWON LIKE '{}%' )""".format(team.nation, team.gender, team.foundDate, team.timesWon)
                cursor.execute(query)
                teams = cursor.fetchall()
                return teams

This function select teams with a specific search. It returns the team table tuples which it found as an array.

* createInitTeams() function of class StoreTeam:

     .. code-block:: python

      def createInitTeams(self, dsn):
         app.storeT = StoreTeam(app.config['dsn'])

         newTeam = team('Turkey', 'Male', '1920', '4')
         app.storeT.addTeam(newTeam, dsn)
         newTeam2 = team('England', 'Male', '1936', '3')
         app.storeT.addTeam(newTeam2, dsn)
         newTeam3 = team('China', 'Male', '1906','5')
         app.storeT.addTeam(newTeam3, dsn)
         newTeam4 = team('Russia', 'Female', '1943','1')
         app.storeT.addTeam(newTeam4, dsn)

This function creates initial elements when database has initialized. It uses add function to create initial tuples.

2.2 class StoreP
++++++++++++++++

* class StoreP init function and createTable() function:

     .. code-block:: python

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

createTable() function works like StoreTeam class' createTable() function.

Also in StoreP functions with .. as context manager of psycopg2 has used.

* addPlayer() function of class StoreP:

     .. code-block:: python

      def addPlayer(self, player, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO PLAYERS (NAME, GENDER, NATION, BIRTHDATE, TEAM) VALUES(%s, %s, %s, %s, %s)", (player.name, player.gender, player.nation, player.birthDate, player.team))

This function works as same as addTeam function of StoreTeam.

* deletePlayer() function of class StoreP:

     .. code-block:: python

      def deletePlayer(self, id, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ DELETE FROM PLAYERS WHERE ID = {}""".format(id)
                cursor.execute(query)

This function works as same as deleteTeam function of StoreTeam.

* updatePlayer() function of class StoreP:

     .. code-block:: python

      def updatePlayer(self, player, id, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """UPDATE PLAYERS SET NAME = '{}', GENDER = '{}', NATION = '{}', BIRTHDATE = '{}', TEAM = '{}' WHERE ID = {} """.format(player.name, player.gender, player.nation, player.birthDate, player.team, id)
                cursor.execute(query)

This function also works as same as updateTeam function of StoreTeam.

* getAllPlayers() function of class StoreP:

     .. code-block:: python

      def getAllPlayers (self, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ SELECT PLAYERS.ID, PLAYERS.NAME, PLAYERS.GENDER, PLAYERS.NATION, PLAYERS.BIRTHDATE, TEAMS.NATION FROM PLAYERS INNER JOIN TEAMS ON TEAMS.ID = PLAYERS.TEAM """
                cursor.execute(query)
                players = cursor.fetchall()
                return players

This function also works as same as getAllTeams() function of StoreTeam.

* selectPlayers() function of class StoreP:

     .. code-block:: python

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

This function also select players with a specific search. The SQL statement
joins the teams and players tables and searches what to search in joined tables. After
that it returns the players table tuples which it found as an array.

* createInitPlayers() function of class StoreP:

     .. code-block:: python

      def createInitPlayers(self,dsn):
        app.store = StoreP(app.config['dsn'])

        newPlayer = player('Hasan', 'Male', 'Turkish', '1994', 1)
        app.store.addPlayer(newPlayer, dsn)
        newPlayer2 = player('Rose', 'Female', 'English', '1995', 2)
        app.store.addPlayer(newPlayer2, dsn)
        newPlayer3 = player('Dimitrov', 'Male', 'Russian', '1993', 4)
        app.store.addPlayer(newPlayer3, dsn)

This function creates initial elements when database has initialized. It uses add function to create initial tuples.

2.3 class StoreTM
+++++++++++++++++

* class StoreTM init function and createTable() function:

     .. code-block:: python

      def __init__(self, dbSettings):
        self.dsn = dbSettings

      def createTable(self, dsn):
        try:
            connection = dbapi2.connect(dsn)
            cursor = connection.cursor()
            statement = """ CREATE TABLE TECHNICMEMBERS (
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(45),
            GENDER VARCHAR(6),
            NATION VARCHAR(45),
            BIRTHDATE VARCHAR(10),
            COACH INTEGER REFERENCES COACHES ON DELETE CASCADE ON UPDATE CASCADE
            )"""
            cursor.execute(statement)
            connection.commit()
            cursor.close()
         except dbapi2.DatabaseError:
            connection.rollback()
         finally:
            connection.close()

createTable() function works like StoreTeam class' createTable() function.

Also in StoreTM functions with .. as context manager of psycopg2 has used.

* addTm() function of class StoreTM:

     .. code-block:: python

      def addTm(self, tm, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO TECHNICMEMBERS (NAME, GENDER, NATION, BIRTHDATE, COACH) VALUES(%s, %s, %s, %s, %s)", (tm.name, tm.gender, tm.nation, tm.birthDate, tm.coach))

This function works as same as addTeam function of StoreTeam.

* deleteTm() function of class StoreTM:

     .. code-block:: python

      def deleteTm(self, id, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ DELETE FROM TECHNICMEMBERS WHERE ID = {}""".format(id)
                cursor.execute(query)

This function works as same as deleteTeam function of StoreTeam.

* updateTm() function of class StoreTM:

     .. code-block:: python

      def updateTm(self, tm, id, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """UPDATE TECHNICMEMBERS SET NAME= '{}', GENDER = '{}', NATION = '{}', BIRTHDATE = '{}', COACH = '{}' WHERE ID = {} """.format(tm.name, tm.gender, tm.nation, tm.birthDate, tm.coach, id)
                cursor.execute(query)

This function also works as same as updateTeam function of StoreTeam.

* getAllTms() function of class StoreTM:

     .. code-block:: python

      def getAllTms (self, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """ SELECT TECHNICMEMBERS.ID, TECHNICMEMBERS.NAME, TECHNICMEMBERS.GENDER, TECHNICMEMBERS.NATION, TECHNICMEMBERS.BIRTHDATE, COACHES.NAME FROM TECHNICMEMBERS INNER JOIN COACHES ON COACHES.ID = TECHNICMEMBERS.COACH """
                cursor.execute(query)
                tms = cursor.fetchall()
                return tms

This function also works as same as getAllTeams() function of StoreTeam.

* selectTms() function of class StoreTM:

     .. code-block:: python

      def selectTms(self, tm, dsn):
        with dbapi2.connect(dsn) as connection:
            with connection.cursor() as cursor:
                query = """SELECT TECHNICMEMBERS.ID, TECHNICMEMBERS.NAME, TECHNICMEMBERS.GENDER, TECHNICMEMBERS.NATION, TECHNICMEMBERS.BIRTHDATE, COACHES.NAME
                FROM TECHNICMEMBERS INNER JOIN COACHES ON COACHES.ID = TECHNICMEMBERS.COACH
                WHERE(TECHNICMEMBERS.NAME LIKE  '{}%' ) AND (TECHNICMEMBERS.GENDER LIKE '{}%' ) AND
                (TECHNICMEMBERS.NATION LIKE '{}%' ) AND (TECHNICMEMBERS.BIRTHDATE LIKE '{}%' ) AND
                (COACHES.NAME LIKE '{}%' ) """.format(tm.name, tm.gender, tm.nation, tm.birthDate, tm.coach)
                cursor.execute(query)
                tms = cursor.fetchall()
                return tms

This function also select players with a specific search. The SQL statement
joins the technicmembers and coaches tables and searches what to search in joined tables. After
that it returns the technicmembers table tuples which it found as an array.

* createInitTMs() function of class StoreTM:

     .. code-block:: python

      def createInitTMs(self, dsn):
        app.storeT = StoreTM(app.config['dsn'])

        newTm = tm('Veli', 'Male', 'Turkish', '1978', 1)
        app.storeT.addTm(newTm, dsn)
        newTm = tm('Ayşe', 'Female', 'Turkish', '1978', 1)
        app.storeT.addTm(newTm, dsn)
        newTm = tm('Jane', 'Female', 'English', '1982', 2)
        app.storeT.addTm(newTm, dsn)

This function creates initial elements when database has initialized. It uses add function to create initial tuples.

3 HTML handling .pys
--------------------

3.1 teams.py
++++++++++++

* Import part of the teams.py file

     .. code-block:: python

      from flask import redirect
      from flask import render_template
      from flask import request
      from flask import url_for

      from config import app
      from team import team
      from store import StoreTeam
      import psycopg2 as dbapi2

redirect, render_template, request and url_for features of Flask web framework have used.
Like in store classes app object of Flask has imported from config. team class has imported.
StoreTeam class has imported from store file. pyscopg2 has imported as a dbapi2 for use as a
database api.

* teams function for rendering teams.html file

     .. code-block:: python

      @app.route('/teams', methods = ['GET', 'POST'])
      def teams():

      dsn = app.config['dsn']

      app.store = StoreTeam(dsn)


      if request.method == 'GET':
         allTeams = app.store.getAllTeams(dsn)

This part of teams function renders the url '/teams' with teams.html file. Uses 'GET' and 'POST' methods.
Uses dsn as a database settings which is implementing in config.py whether ElephantSQL or
Vagrant database system. app.store variable assigned to a StoreTeam object. All StoreTeam object
methods can be used via app.store variable. If request.method equals to 'GET' method getAllTeams
function of StoreTeam object has invoked and gets all teams as and array and passed them to html file.
After all operations allTeams variable assigned to an array which holds all the teams data. At the end
of the function allTeams variable send to html file for listing.

* delete method

     .. code-block:: python

      elif 'delete' in request.form:
         ids = request.form.getlist('teams')
         for id in ids:
            app.store.deleteTeam(id, dsn)
         allTeams = app.store.getAllTeams(dsn)

If request method from user is delete this part of teams function has invoked. It gets the clicked checkbox ids
and passed that ids one by one to the deleteTeam() function of StoreTeam class. After that tuples get deleted.

* add method

     .. code-block:: python

      elif 'add' in request.form:
         nation = request.form['nationToAdd']
         gender = request.form['genderToAdd']
         foundDate = request.form['foundDateToAdd']
         timesWon = request.form['timesWonToAdd']
         newTeam = team(nation, gender, foundDate, timesWon)
         app.store.addTeam(newTeam, dsn)
         allTeams = app.store.getAllTeams(dsn)

If request method from user is add this part of teams function has invoked. Datas in the add textboxes has passed as a
attributes of a team object and addTeam function of StoreTeam class added the tuple using team object attributes as a
tuple attributes.

* update method

     .. code-block:: python

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

If request method from user is update this part of teams function has invoked. Datas in update textboxes has passed as a
attributes of a team object and id of the tuple that needs to be update. After that updateTeam function StoreTeam class updated
the necessary tuple using team object attributes as a tuple attributes.

* find method

     .. code-block:: python

      elif 'find' in request.form:
         nation = request.form['nationToFind']
         gender = request.form['genderToFind']
         foundDate = request.form['foundDateToFind']
         timesWon = request.form['timesWonToFind']
         findTeam = team(nation, gender, foundDate, timesWon)
         allTeams = app.store.selectTeams(findTeam, dsn)


      return render_template('teams.html', teams = allTeams)

Finally if request method from user is find this part of teams function has invoked. Datas in find textboxes has passed as a
attributes of a team object and selectTeams function of StoreTeam find the searched datas with SQL operation in the database and
returns an array of teams that found.

At the end of function teams.html file rendered with this python code and allTeams attribute passed to html file to be listed.

3.2 players.py
++++++++++++++

* Import part of the players.py file

     .. code-block:: python

      from flask import redirect
      from flask import render_template
      from flask import request
      from flask import url_for

      from config import app
      from player import player
      from store import StoreP
      from store import StoreTeam
      import psycopg2 as dbapi2

Like in teams.py file necessary imports for Flask web framework use has implemented.
player class has imported. Both StoreP and StoreTeam classes has imported because of the
team foreign key in the players table. After all operations allPlayers variable assigned to an array which holds allPlayers data as well. At the end
of the function allPlayers variable send to html file for listing and also allTeams variable too.

* players function for rendering players.html file

     .. code-block:: python

      @app.route('/players', methods = ['GET', 'POST'])
      def players():

         dsn = app.config['dsn']

         app.store = StoreP(dsn)

         app.storeT = StoreTeam(dsn)
         allTeams = app.storeT.getAllTeams(dsn)

         if request.method == 'GET':
            allPlayers = app.store.getAllPlayers(dsn)

This part of players function works as same as teams function in teams.py file. With a little difference
it has another app.storeT variable for using StoreTeam class for getting all teams for foreign key of
players table team attribute.

* delete method

     .. code-block:: python

      elif 'delete' in request.form:
        ids = request.form.getlist('players')
        for id in ids:
            app.store.deletePlayer(id, dsn)
        allPlayers = app.store.getAllPlayers(dsn)

This part of players function works as same as teams function of teams.py file.

* add method

     .. code-block:: python

      elif 'add' in request.form:
        name = request.form['nameToAdd']
        gender = request.form['genderToAdd']
        nation = request.form['nationToAdd']
        birthDate = request.form['birthDateToAdd']
        team = request.form['teamToAdd']
        newPlayer = player(name, gender, nation, birthDate, team)
        app.store.addPlayer(newPlayer, dsn)
        allPlayers = app.store.getAllPlayers(dsn)

This part of players function also works as same as teams function of teams.py file.

* update method

     .. code-block:: python

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

Also this part of players function works as same as teams function in teams.py


* find method

     .. code-block:: python

      elif 'find' in request.form:
        name = request.form['nameToFind']
        gender = request.form['genderToFind']
        nation = request.form['nationToFind']
        birthDate = request.form['birthDateToFind']
        team = request.form['teamToFind']
        findPlayer = player(name, gender, nation, birthDate, team)
        allPlayers = app.store.selectPlayers(findPlayer, dsn)


      return render_template('players.html', players = allPlayers, teams = allTeams )

Final part is also same as teams function in teams.py file.

At the end of function players.html file rendered with this python code and allPlayers and allTeams attribute passed to html file to be listed.

3.3 technicmembers.py
+++++++++++++++++++++

* Import part of the technicmembers.py file

     .. code-block:: python

      from flask import redirect
      from flask import render_template
      from flask import request
      from flask import url_for

      from config import app
      from technicmember import tm
      from store import StoreTM
      import psycopg2 as dbapi2

      import coaches

Like in teams.py file necessary imports for Flask web framework use has implemented.
tm class has imported. StoreTM class has imported and also coaches has imported because of the
coach foreign key in the technicmembers table. After all operations allTms variable assigned to an array which holds allTms data as well. At the end
of the function allTms variable send to html file for listing and also allCoaches variable too.

* technicmembers function for rendering technicMembers.html file

     .. code-block:: python

      @app.route('/technicMembers', methods = ['GET', 'POST'])
      def technicMembers():

         dsn = app.config['dsn']

         app.store = StoreTM(dsn)

         allCoaches = coaches.get_coaches()

         if request.method == 'GET':
            allTms = app.store.getAllTms(dsn)

This part of technicmembers function works as same as teams function in teams.py file. With a little difference
it has allCoaches variable for using getting all coaches from coaches file with coaches.get_coaches function for foreign key of
technicmembers table coach attribute.

* delete method

     .. code-block:: python

      elif 'delete' in request.form:
        ids = request.form.getlist('tms')
        for id in ids:
            app.store.deleteTm(id, dsn)
        allTms = app.store.getAllTms(dsn)

This part of technicmembers function works as same as teams function of teams.py file.

* add method

     .. code-block:: python

      elif 'add' in request.form:
        name = request.form['nameToAdd']
        gender = request.form['genderToAdd']
        nation = request.form['nationToAdd']
        birthDate = request.form['birthDateToAdd']
        coach = request.form['coachToAdd']
        newTm = tm(name, gender, nation, birthDate, coach)
        app.store.addTm(newTm, dsn)
        allTms = app.store.getAllTms(dsn)

This part of technicmembers function also works as same as teams function of teams.py file.

* update method

     .. code-block:: python

      elif 'update' in request.form:
        ids = request.form.getlist('tms')
        id = ids[0]
        name = request.form['nameToUpdate']
        gender = request.form['genderToUpdate']
        nation = request.form['nationToUpdate']
        birthDate = request.form['birthDateToUpdate']
        coach = request.form['coachToUpdate']
        newTm = tm(name, gender, nation, birthDate, coach)
        app.store.updateTm(newTm, id, dsn)
        allTms = app.store.getAllTms(dsn)

Also this part of technicmembers function works as same as teams function in teams.py


* find method

     .. code-block:: python

      elif 'find' in request.form:
        name = request.form['nameToFind']
        gender = request.form['genderToFind']
        nation = request.form['nationToFind']
        birthDate = request.form['birthDateToFind']
        coach = request.form['coachToFind']
        findTm = tm(name, gender, nation, birthDate, coach)
        allTms = app.store.selectTms(findTm, dsn)


      return render_template('technicMembers.html', tms = allTms, coaches = allCoaches )

Final part is also same as teams function in teams.py file.

At the end of function technicMembers.html file rendered with this python code and allTms and allCoaches attribute passed to html file to be listed.