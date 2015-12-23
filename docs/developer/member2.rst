Parts Implemented by Alican MERTAN
==================================

Database Design
***************


1 Tables
--------

1.1 Tournaments Table
+++++++++++++++++++++

* Tournaments table keeping records of the tournaments data


                +---------------+------------+
                | Name          | Type       |
                +===============+============+
                | ID            | INTEGER    |
                +---------------+------------+
                |NAME           | VARCHAR    |
                +---------------+------------+
                |YEAR           | VARCHAR    |
                +---------------+------------+
                |WINNER         | INTEGER    |
                +---------------+------------+
                |BEST_PLAYER    | INTEGER    |
                +---------------+------------+

* *name* keeps the record of name of the given tournament.
* *year* keeps the record of year of the given tournament.
* *winner* keeps the record of the winner of the given tournament. It references the *teams* table.
* *best_player* keeps the record of the best player of the given tournament. It references the *players* table.


**Sql statement that initialize the tournaments table**:

 .. code-block:: sql

    CREATE TABLE TOURNAMENTS(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        YEAR VARCHAR(4),
        WINNER INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
        BEST_PLAYER INTEGER REFERENCES PLAYERS ON DELETE CASCADE ON UPDATE CASCADE
        )


1.2 Matches Table
+++++++++++++++++

* Matches table keeping records of the matches data


                +---------------+------------+
                | Name          | Type       |
                +===============+============+
                | ID            | INTEGER    |
                +---------------+------------+
                |TOURNAMENT     | INTEGER    |
                +---------------+------------+
                |TEAM1          | INTEGER    |
                +---------------+------------+
                |TEAM2          | INTEGER    |
                +---------------+------------+
                |SCORE          | VARCHAR    |
                +---------------+------------+

* *tournament* keeps the record of name of the tournament for given match. It references the *tournaments* table.
* *team1* keeps the record of name of the team for given match. It references the *teams* table.
* *team2* keeps the record of name of the team for given match. It references the *teams* table.
* *score* keeps the record of the score of the given match.


**Sql statement that initialize the matches table**:

 .. code-block:: sql

    CREATE TABLE MATCHES(
        ID SERIAL PRIMARY KEY,
        TOURNAMENT INTEGER REFERENCES TOURNAMENTS ON DELETE CASCADE ON UPDATE CASCADE,
        TEAM1 INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
        TEAM2 INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
        SCORE VARCHAR(3)
        )

Code
****

1 Functions
-----------

1.1 creating tables
+++++++++++++++++++

create_table functions used in order to create tables.

* create_table function in tournaments.py:

   .. code-block:: python

      def create_table():
          try:
              cursor = create_connection()
              statement = """ CREATE TABLE TOURNAMENTS(
              ID SERIAL PRIMARY KEY,
              NAME VARCHAR(45),
              YEAR VARCHAR(4),
              WINNER INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
              BEST_PLAYER INTEGER REFERENCES PLAYERS ON DELETE CASCADE ON UPDATE CASCADE
              )"""
              cursor.execute(statement)
              cursor.connection.commit()
              close_connection(cursor)
          except psycopg2.DatabaseError:
              cursor.connection.rollback()
          finally:
              cursor.connection.close()

* create_table function in matches.py:

   .. code-block:: python

      def create_table():
          try:
              cursor = create_connection()
              statement = """ CREATE TABLE MATCHES(
              ID SERIAL PRIMARY KEY,
              TOURNAMENT INTEGER REFERENCES TOURNAMENTS ON DELETE CASCADE ON UPDATE CASCADE,
              TEAM1 INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
              TEAM2 INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE,
              SCORE VARCHAR(3)
              )"""
              cursor.execute(statement)
              cursor.connection.commit()
              close_connection(cursor)
           except psycopg2.DatabaseError:
              cursor.connection.rollback()
           finally:
              cursor.connection.close()

1.2 initiliazing database
+++++++++++++++++++++++++

create_init functions used in order to initiliaze database with some tupples.

* create_init_tournaments function in tournaments.py:

   .. code-block:: python

      def create_init_tournaments():

        add_new_tournament('World Cup', '2015', 1, 1)
        add_new_tournament('World Cup', '2014', 2, 3)
        add_new_tournament('World Cup', '2013', 3, 2)

* create_init_matches function in matches.py:

   .. code-block:: python

      def create_init_matches():

         add_new_match(1, 1, 2, '5-3')
         add_new_match(1, 3, 4, '4-2')
         add_new_match(1, 3, 2, '2-6')

1.3 adding new tupples
++++++++++++++++++++++

add_new functions used in order to add new tupples to a table. Function gets attribute values as a parameter.

* add_new_tournament function in tournaments.py:

   .. code-block:: python

    def add_new_tournament(name, year, winner, best_player):
      cursor = create_connection()

      cursor.execute("INSERT INTO tournaments (name, year, winner, best_player) VALUES (%s, %s, %s, %s)", (name, year, winner, best_player))
      cursor.connection.commit()

      close_connection(cursor)

      return True

* add_new_match function in matches.py:

   .. code-block:: python

     def add_new_match(tournament, team1, team2, score):
        cursor = create_connection()

        cursor.execute("INSERT INTO matches (tournament, team1, team2, score) VALUES (%s, %s, %s, %s)", (tournament, team1, team2, score))
        cursor.connection.commit()

        close_connection(cursor)

        return True

1.4 deleting tupples
++++++++++++++++++++

delete functions used in order to delete tupples. Function takes primary key value as a parameter.

* delete_tournament function in tournaments.py:

.. code-block:: python

   def delete_tournament(id):
    cursor = create_connection()
    statement = """DELETE FROM TOURNAMENTS WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

* delete_match function in matches.py:

.. code-block:: python

   def delete_match(id):
    cursor = create_connection()
    statement = """DELETE FROM MATCHES WHERE ID={}""".format(id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

1.5 updating tupples
++++++++++++++++++++

update functions used in order to update selected tupples. Function takes primary key as a parameter to find
 selected tupple and takes attributes values as a paramater to update tupple.

* update_tournament function in tournaments.py:

.. code-block:: python

   def update_tournament(id, nameUpdate, yearUpdate, winnerUpdate, best_playerUpdate):
    cursor = create_connection()
    statement = """UPDATE TOURNAMENTS SET NAME = '{}', YEAR = '{}', WINNER = '{}', BEST_PLAYER = {} WHERE ID={} """.format(nameUpdate, yearUpdate, winnerUpdate, best_playerUpdate, id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

* update_match function in matches.py:

.. code-block:: python

   def update_match(id, tournamentUpdate, team1Update, team2Update, scoreUpdate):
    cursor = create_connection()
    statement = """UPDATE MATCHES SET TOURNAMENT = '{}', TEAM1 = '{}', TEAM2 = '{}', SCORE = '{}' WHERE ID={} """.format(tournamentUpdate, team1Update, team2Update, scoreUpdate, id)
    cursor.execute(statement)
    cursor.connection.commit()

    close_connection(cursor)

1.6 finding tupples
+++++++++++++++++++

findInJointTables functions used in order to query tupples. Function takes attribute values as a parameter and
returns tupples as an array. If an empty search made, all the tupples will be returned.

* findInJointTables function in tournaments.py:

.. code-block:: python

   def findInJointTables(nameFind, yearFind, winnerFind, best_playerFind):
    statement= """ SELECT TOURNAMENTS.ID, TOURNAMENTS.NAME, YEAR, TEAMS.NATION , PLAYERS.NAME FROM TOURNAMENTS INNER JOIN PLAYERS ON PLAYERS.ID=TOURNAMENTS.BEST_PLAYER INNER JOIN TEAMS ON TEAMS.ID=TOURNAMENTS.WINNER WHERE(TOURNAMENTS.NAME LIKE  '{}%' ) AND (YEAR LIKE '{}%' ) AND (TEAMS.NATION LIKE '{}%' )  AND (PLAYERS.NAME LIKE '{}%' )""".format(nameFind, yearFind, winnerFind, best_playerFind)

    cursor = create_connection()
    cursor.execute(statement)
    tournaments = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return tournaments

* findInJointTables function in matches.py:

.. code-block:: python

   def findInJointTables(tournamentFind, team1Find, team2Find, scoreFind):
    statement= """ SELECT MATCHES.ID, TOURNAMENTS.NAME, t1.NATION, t2.NATION, MATCHES.SCORE FROM MATCHES INNER JOIN TOURNAMENTS ON TOURNAMENTS.ID=MATCHES.TOURNAMENT INNER JOIN TEAMS t1 ON t1.ID=MATCHES.TEAM1 INNER JOIN TEAMS t2 ON t2.ID=MATCHES.TEAM2 WHERE(TOURNAMENTS.NAME LIKE  '{}%' ) AND (t1.NATION LIKE '{}%' ) AND (t2.NATION LIKE '{}%' )  AND (MATCHES.SCORE LIKE '{}%' )""".format(tournamentFind, team1Find, team2Find, scoreFind)

    cursor = create_connection()
    cursor.execute(statement)
    matches = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)

    return matches

1.7 fetching all tupples
++++++++++++++++++++++++

showJointTables functions used in order to fetch all the tupples. Function returns tupples as an array.

* showJointTables function in tournaments.py:

.. code-block:: python

   def showJointTables():
    cursor = create_connection()
    statement= """ SELECT TOURNAMENTS.ID, TOURNAMENTS.NAME, YEAR, TEAMS.NATION , PLAYERS.NAME FROM TOURNAMENTS INNER JOIN PLAYERS ON PLAYERS.ID=TOURNAMENTS.BEST_PLAYER INNER JOIN TEAMS ON TEAMS.ID=TOURNAMENTS.WINNER  """
    cursor.execute(statement)
    tournaments = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)
    return tournaments

* showJointTables function in matches.py:

.. code-block:: python

   def showJointTables():
    cursor = create_connection()
    statement= """ SELECT MATCHES.ID, TOURNAMENTS.NAME, t1.NATION, t2.NATION, MATCHES.SCORE FROM MATCHES INNER JOIN TOURNAMENTS ON TOURNAMENTS.ID=MATCHES.TOURNAMENT INNER JOIN TEAMS t1 ON t1.ID = MATCHES.TEAM1 INNER JOIN TEAMS t2 ON t2.ID=MATCHES.TEAM2 """
    cursor.execute(statement)
    matches = cursor.fetchall()
    cursor.connection.commit()

    close_connection(cursor)
    return matches

2 HTML handling
---------------

tournaments() and matches() functions used in order to handle HTML related works.

* tournaments function in tournaments.py:

.. code-block:: python

   @app.route("/tournaments/", methods=['GET', 'POST'])
   def tournaments():

    dsn = app.config['dsn']

    app.storeT = StoreTeam(dsn)
    allTeams = app.storeT.getAllTeams(dsn)

    app.store = StoreP(dsn)
    allPlayers = app.store.getAllPlayers(dsn)

    if request.method == 'GET':

        all_tournaments = showJointTables()
        queriedTournaments = findInJointTables('?','?','?','?')

* matches function in matches.py:

.. code-block:: python

   @app.route("/matches", methods=['GET', 'POST'])
   def matches():


    allTournaments = tournaments.get_tournaments()

    dsn = app.config['dsn']

    app.storeT = StoreTeam(dsn)
    allTeams = app.storeT.getAllTeams(dsn)


    if request.method == 'GET':
        all_matches = showJointTables()
        queriedMatches = findInJointTables('?','?','?','?')

2.1 add block
+++++++++++++

In the add block, add_new functions called with the parameters from HTML.

* add block in tournaments.py:

.. code-block:: python

   elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        year = request.form['year']
        winner = request.form['winner']
        best_player = request.form['best_player']
        # ----------------------------------------------

        add_new_tournament(name, year, winner, best_player) # save to db


        all_tournaments = showJointTables()
        queriedTournaments = findInJointTables('?','?','?','?')

* add block in matches.py:

.. code-block:: python

    elif 'add' in request.form:
        # ----------------------------------------------
        tournament = request.form['tournament']
        team1 = request.form['team1']
        team2 = request.form['team2']
        score = request.form['score']
        # ----------------------------------------------

        add_new_match(tournament, team1, team2, score) # save to db

        all_matches = showJointTables() # get all matches
        queriedMatches = findInJointTables('?','?','?','?')

2.2 delete block
++++++++++++++++

In the delete block, delete functions called with the parameters from HTML.

* delete block in tournaments.py:

.. code-block:: python

    elif 'delete' in request.form:
        ids = request.form.getlist('tournaments_to_delete')
        for id in ids:
            delete_tournament(id)
        all_tournaments = showJointTables()
        queriedTournaments = findInJointTables('?','?','?','?')

* delete block in matches.py:

.. code-block:: python

   elif 'delete' in request.form:
        ids = request.form.getlist('matches_to_delete')
        for id in ids:
            delete_match(id)
        all_matches = showJointTables()
        queriedMatches = findInJointTables('?','?','?','?')

2.3 find block
++++++++++++++

In the find block, findInJointTables functions called with the parameters from HTML.

* find block in tournaments.py:

.. code-block:: python

   elif 'find' in request.form:
        nameFind = request.form['nameFind']
        yearFind = request.form['yearFind']
        winnerFind = request.form['winnerFind']
        best_playerFind = request.form['best_playerFind']

        all_tournaments = showJointTables()
        queriedTournaments = findInJointTables(nameFind,yearFind,winnerFind,best_playerFind)

* find block in matches.py:

.. code-block:: python

       elif 'find' in request.form:
        tournamentFind = request.form['tournamentFind']
        team1Find = request.form['team1Find']
        team2Find = request.form['team2Find']
        scoreFind = request.form['scoreFind']

        all_matches = showJointTables()
        queriedMatches = findInJointTables(tournamentFind, team1Find, team2Find, scoreFind)


2.4 update block
++++++++++++++++

In the update block, update functions called with the parameters from HTML.

* update block in tournaments.py:

.. code-block:: python

     elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            nameUpdate = request.form['nameUpdate'+id]
            yearUpdate = request.form['yearUpdate'+id]
            winnerUpdate = request.form['winnerUpdate'+id]
            best_playerUpdate = request.form['best_playerUpdate'+id]
            update_tournament(id, nameUpdate, yearUpdate, winnerUpdate, best_playerUpdate)

        all_tournaments = showJointTables()
        queriedTournaments = findInJointTables('?','?','?','?')

* update block in matches.py:

.. code-block:: python

     elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            tournamentUpdate = request.form['tournamentUpdate'+id]
            team1Update = request.form['team1Update'+id]
            team2Update = request.form['team2Update'+id]
            scoreUpdate = request.form['scoreUpdate'+id]
            update_match(id, tournamentUpdate, team1Update, team2Update, scoreUpdate)










