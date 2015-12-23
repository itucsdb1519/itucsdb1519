Parts Implemented by Ahmet Yılmaz
=================================

Database Design
***************


1 Tables
--------

1.1 Coaches Table
+++++++++++++++++

* Coaches table keeping record of the coaches data


                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | ID            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |NAME           | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |GENDER         | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |NATIONALITY    | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |BIRTH_DATE     | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |CURRENT_TEAM   | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+

* *name* keeps the record of name of the given coach.
* *gender* keeps the record of gender of the given coach.
* *nationality* keeps the record of the nationality of the given coach.
* *birth_date* keeps the record of birth date of the given coach.
* *current_team* keeps the record of current team of the given coach which refers to teams table.

**Sql statement that initialize the coaches table**:

 .. code-block:: sql

    CREATE TABLE COACHES(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(45),
        GENDER VARCHAR(6),
        NATIONALITY VARCHAR(45),
        BIRTH_DATE  VARCHAR(10),
        CURRENT_TEAM INTEGER REFERENCES TEAMS ON DELETE CASCADE ON UPDATE CASCADE
        )

1.2 Player Statistics Table
+++++++++++++++++++++++++++

* Player Statistics table keeping record of the statistics data of players.


                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | ID            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |PLAYER         | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |MATCHES_PLAYED | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |MATCHES_WON    | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |WIN_RATE       | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |AVERAGE_SCORE  | INTEGER    |   0       |  0        |
                +---------------+------------+-----------+-----------+
* *player* keeps the record of name of the given player refers to players table on delete and on update cascades
* *matches_played* keeps the count of played matches of given player.
* *matches_won* keeps the count of won matches of given player.
* *win_rate* keeps the record of win rate of the given player.
* *average_score* keeps the record of average score of the given player according to matches he/she played.


**Sql statement that initialize the playerstatistics table**:

 .. code-block:: sql

    CREATE TABLE PLAYERSTATISTICS(
        ID SERIAL PRIMARY KEY,
        matches_played VARCHAR(10),
        matches_won VARCHAR(10),
        win_rate VARCHAR(10),
        average_score  VARCHAR(10),
        player INTEGER REFERENCES players ON DELETE CASCADE ON UPDATE CASCADE
        )


1.3 Users Table
+++++++++++++++

* Users table keeping record of the users data


                +---------------+------------+-----------+-----------+
                | Name          | Type       | Not Null  |Primary K. |
                +===============+============+===========+===========+
                | ID            | INTEGER    |   0       |  1        |
                +---------------+------------+-----------+-----------+
                |USERNAME       | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+
                |PASSWORD       | VARCHAR    |   0       |  0        |
                +---------------+------------+-----------+-----------+

* *username* keeps the record of name of the given user.
* *password* keeps the record of gender of the given user.


**Sql statement that initialize the technic members table**:

 .. code-block:: sql

    CREATE TABLE USERS(
        ID SERIAL PRIMARY KEY,
        USERNAME VARCHAR(45),
        PASSWORD VARCHAR(6)
        )

Code
****


1 Python Flask Extension Parts
------------------------------

coaches.py
++++++++++

* Import part of the coaches.py file

     .. code-block:: python

      from flask import request
      from flask import render_template
      from config import app
      from config import create_connection, close_connection
      import psycopg2
      import teams
      from store import StoreTeam

render_template and request features of Flask web framework have used.
app object of Flask has imported from config.
team class and StoreTeam class has imported. Since "corrent_team" attribure refers to teams table
pyscopg2 has imported as a dbapi2 for use as a database api.

* route function of coaches for rendering teams.html file

     .. code-block:: python

      @app.route("/coaches/", methods=['GET', 'POST'])
      def coaches():
      dsn = app.config['dsn']

      app.store = StoreTeam(dsn)
      all_teams = app.store.getAllTeams(dsn)

      if request.method == 'GET':
        all_coaches = join_tables()

This part of coaches function renders the url '/teams' with coaches.html file. Uses 'GET' and 'POST' methods.
Uses dsn as a database settings which is implementing in config.py whether ElephantSQL or
Vagrant database system. To get all teams for joint tables first getAllTeams function used and teams assigned to all_teams variable.
after that join_tables function used to join teams and coaches tables to get meaningful data and assigned to all_coaches variable.


* delete method

     .. code-block:: python

      elif 'delete' in request.form:
        ids = request.form.getlist('coaches_to_delete')
        for id in ids:
            delete_coach(id)

        all_coaches = join_tables()


If request method is delete which means if delete button has clicked on html page. Code requests checked box information and assign this to a list called ids.
Then each element in ids list sent to delete_coach function which deletes tuple from table. Then all_coaches variable renewed with remaining tuples.

* add method

     .. code-block:: python

      elif 'add' in request.form:
        # ----------------------------------------------
        name = request.form['name']
        gender = request.form['gender']
        nationality = request.form['nationality']
        birth_date = request.form['birth_date']
        current_team = request.form['current_team']
        # ----------------------------------------------

        add_new_coach(name, gender, nationality, birth_date, current_team) # save to db

        all_coaches = join_tables()

If request method is add which means add button has clicked on html page. Code requests the values entered in textboxes.
These values sent to add_new_coach function which adds the tuple with according values to the table. New all tuples fetched to print to the screen

* update method

     .. code-block:: python

      elif 'update' in request.form:
        ids = request.form.getlist('update')
        for id in ids:
            name_update = request.form['name_update'+id]
            gender_update = request.form['gender_update'+id]
            nationality_update = request.form['nationality_update'+id]
            birth_date_update = request.form['birth_date_update'+id]
            current_team_update = request.form['current_team_update'+id]

            update_coach(id,name_update,gender_update,nationality_update,birth_date_update,current_team_update)

        all_coaches = join_tables()

If request method is update which means if update button clicked on html page. Code requests the values entered in textboxes and
gets the ids with checkedboxes. for each id tuples changed with new values. New all tuples fetched to print to the screen.

* find method

     .. code-block:: python

      elif 'find' in request.form:
        para_1 = request.form['name_find']
        para_2 = request.form['gender_find']
        para_3 = request.form['nationality_find']
        para_4 = request.form['birth_date_find']
        para_5 = request.form['current_team_find']

        all_coaches = find_coach(para_1,para_2,para_3,para_4,para_5)


Else if request method is find which means find button clicked on html page. Code requests the values from textboxes for attributes.
values sent to find_coach function to select according tuples from table and print.

* showall method

     .. code-block:: python

      elif 'showall' in request.form:

        all_coaches = join_tables()

Else if request method is showall which means Show All button has clicked on html page. Coaches table and teams table joint to
show all coaches tables tuples with according curent_team value.

     .. code-block:: python

      return render_template("coaches.html", coaches=all_coaches, teams_select=all_teams)

Route function returns render_template function which gets all coaches and send them to html page to print to the screen.

playerstatistics.py
+++++++++++++++++++

Same things did as did in coaches.py
But playerstatistics table has a different foreign key which refers to players table

users.py
++++++++

Same things did as did in coaches.py

2 Python PostgreSql Parts
-------------------------

coaches.py
++++++++++


* get_coaches function

      .. code-block:: python

         def get_coaches():
             cursor = create_connection()

             cursor.execute("SELECT * FROM coaches;")
             coaches = cursor.fetchall()

             close_connection(cursor)

             return coaches


This function selects all tuples from table without condition.


* create_init_coaches function

      .. code-block:: python

         def create_init_coaches():

             add_new_coach('Zehra', 'female', 'turkish', '1964', 1)
             add_new_coach('Mike', 'male', 'english', '1954', 2)
             add_new_coach('Chan', 'male', 'chinese', '1962', 3)



This function adds 3 initial tuple when initialize database function called using add_new_coach function.


* update_coach function

      .. code-block:: python

         def update_coach(id, name_update, gender_update, nationality_update, birth_date_update, current_team_update):
             cursor = create_connection()
             statement = """UPDATE COACHES SET NAME = '{}', GENDER = '{}', NATIONALITY = '{}', BIRTH_DATE = '{}', CURRENT_TEAM = '{}' WHERE ID = {}""".format(name_update, gender_update, nationality_update, birth_date_update, current_team_update,id)
             cursor.execute(statement)
             cursor.connection.commit()

             close_connection(cursor)

This function updates tuples with values coming from html page.

* find_coach function

      .. code-block:: python

        def find_coach(name_find, gender_find, nationality_find, birth_date_find, current_team_find):
            statement= """ SELECT COACHES.ID, COACHES.NAME, COACHES.GENDER, NATIONALITY, BIRTH_DATE, TEAMS.NATION FROM COACHES INNER JOIN TEAMS ON TEAMS.ID=COACHES.CURRENT_TEAM WHERE(COACHES.NAME LIKE  '{}%' ) AND (COACHES.GENDER LIKE '{}%' ) AND (NATIONALITY LIKE '{}%' ) AND (BIRTH_DATE LIKE '{}%' ) AND (TEAMS.NATION LIKE '{}%' )""".format(name_find, gender_find, nationality_find, birth_date_find, current_team_find)

            cursor = create_connection()
            cursor.execute(statement)
            coaches = cursor.fetchall()
            cursor.connection.commit()

            close_connection(cursor)

            return coaches

This function finds tuples with values coming from html page.

* add_new_coach function

      .. code-block:: python

        def add_new_coach(name, gender, nationality, birth_date, current_team):
            cursor = create_connection()

            cursor.execute("INSERT INTO coaches (name, gender, nationality, birth_date, current_team) VALUES (%s, %s, %s, %s, %s)", (name, gender, nationality, birth_date, current_team))
            cursor.connection.commit()

            close_connection(cursor)

            return True

This function adds a new tuple to table with given values from html page.


* delete_coach function

      .. code-block:: python

        def delete_coach(id):
            cursor = create_connection()
            statement = """DELETE FROM COACHES WHERE ID={}""".format(id)
            cursor.execute(statement)
            cursor.connection.commit()

            close_connection(cursor)

This function deletes the tuples from table which selected with checkboxes from html page.



* join_tables function

      .. code-block:: python

        def join_tables():
            cursor = create_connection()
            statement= """ SELECT COACHES.ID, COACHES.NAME, COACHES.GENDER, NATIONALITY, BIRTH_DATE, TEAMS.NATION FROM COACHES INNER JOIN TEAMS ON TEAMS.ID=COACHES.CURRENT_TEAM  """
            cursor.execute(statement)
            coaches = cursor.fetchall()
            cursor.connection.commit()

            close_connection(cursor)
            return coaches

This function joins coaches and teams table for current_team value of coaches table can be printed with the vale it refers.


playerstatistics.py
+++++++++++++++++++

Same things did as did in coaches.py
But playerstatistics table has a different foreign key which refers to players table

users.py
++++++++

Same things did as did in coaches.py
