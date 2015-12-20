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

MVC pattern tried to use in the implementation of teams, players and technic members tables
in web application. For all tables classes implemented. Instances of those classes keep the
data of one tuple. Objects are implemented via html sending parameters and objects are sending
to the functions of store classes and table classes' attributes implement the database tables via store
classes' functions.

* Teams table class :
   .. code-block:: python

      class team:
         def __init__(self, nation, gender, foundDate, timesWon):
            self.nation = nation
            self.gender = gender
            self.foundDate = foundDate
            self.timesWon = timesWon

* Players table class :
   .. code-block:: python

      class player:
         def __init__(self, name, gender, nation, birthDate, team):
            self.name = name
            self.gender = gender
            self.nation = nation
            self.birthDate = birthDate
            self.team = team

* Technic members table class :
   .. code-block:: python

      class tm:
         def __init__(self, name, gender, nation, birthDate, coach):
            self.name = name
            self.gender = gender
            self.nation = nation
            self.birthDate = birthDate
            self.coach = coach