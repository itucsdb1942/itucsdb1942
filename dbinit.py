import os
import sys

import psycopg2 as dbapi2


url="postgres://dneperyi:l94XrLU-lOV2MOaQOPBnoYqVdKreucNZ@manny.db.elephantsql.com:5432/dneperyi"

INIT_STATEMENTS = [

    """ CREATE DOMAIN SCORES AS FLOAT
            CHECK((VALUE>=0.0) AND (VALUE<=10.0)) DEFAULT 0.0;""",
        """CREATE TABLE channel( 
                ID SERIAL PRIMARY KEY,
                chan_name VARCHAR(40)
        )""",

       """ CREATE TABLE season (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(80) NOT NULL,
            season_n INTEGER,
            episode_n VARCHAR(80)
        )""",

        """CREATE TABLE tvseries (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(80) NOT NULL,
            CHANNELID INTEGER REFERENCES channel(id),
            LANGUAGE VARCHAR(80),
            YEAR INTEGER,
            GENRE VARCHAR(80),
            VOTE INTEGER DEFAULT 0,
            SCORE SCORES
        )""",

       """ CREATE TABLE books(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(80),
            WRITER VARCHAR(80),
            PUB_YEAR INTEGER,
            T_PAGE INTEGER,
            PUBLISHER VARCHAR(80),
            LANGUAGE VARCHAR(80),
            GENRE VARCHAR(80),
            SCORE SCORES DEFAULT 0,
            VOTE INTEGER DEFAULT 0)""",
    
   
]

#dsn = """user='postgres' password='docker'
 #       host='localhost' port=5432 dbname='mydatabase'"""


def initialize(url):
    for statement in INIT_STATEMENTS:
        try:
            connection = dbapi2.connect(url)
            cursor = connection.cursor()
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            print("lol")
            connection.rollback()
        finally:
            connection.close()

if __name__ == "__main__":
    print(44)
else:
    initialize(url)

