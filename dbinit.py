import os
import sys

import psycopg2 as dbapi2


url="postgres://dneperyi:l94XrLU-lOV2MOaQOPBnoYqVdKreucNZ@manny.db.elephantsql.com:5432/dneperyi"

INIT_STATEMENTS = [

    """ CREATE DOMAIN SCORES AS FLOAT
            CHECK((VALUE>=0.0) AND (VALUE<=10.0)) DEFAULT 0.0;""",
        """CREATE TABLE channel( 
                ID SERIAL PRIMARY KEY,
                chan_name  VARCHAR(40) UNIQUE
        );""",

       """ CREATE TABLE season (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(80) UNIQUE NOT NULL,
            season_n INTEGER,
            episode_n VARCHAR(80)
        );""",

        """CREATE TABLE tvseries (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(80) UNIQUE NOT NULL,
            CHANNELID INTEGER REFERENCES channel(id),
            LANGUAGE VARCHAR(80),
            YEAR INTEGER,
            GENRE VARCHAR(80),
            VOTE INTEGER DEFAULT 0,
            SCORE SCORES
        );""",

       """ CREATE TABLE books(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(80) UNIQUE NOT NULL,
            WRITERID INTEGER REFERENCES writer(id),
            PUB_YEAR INTEGER,
            T_PAGE INTEGER,
            PUBLISHERID INTEGER REFERENCES publisher(id),
            LANGUAGE VARCHAR(80),
            GENREID INTEGER REFERENCES genre(id),
            SCORE SCORES DEFAULT 0,
            VOTE INTEGER DEFAULT 0);""",
         """CREATE TABLE publisher( 
                ID SERIAL PRIMARY KEY,
                pub_name  VARCHAR(40) UNIQUE,
                pub_country VARCHAR(40)
        );""",
        """CREATE TABLE writer(
            ID SERIAL PRIMARY KEY,
            wr_name VARCHAR(50) NOT NULL,
            wr_middle VARCHAR(50),
            Wr_last VARCHAR(50),
            wr_country VARCHAR(50)
        );""",
        """CREATE TABLE genre(
            ID SERIAL PRIMARY KEY,
            genre_name VARCHAR(50),
            book_id INTEGER REFERENCES books(ID)
        );"""
    
   
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
            connection.rollback()
        finally:
            connection.close()

if __name__ == "__main__":
    print()
else:
    initialize(url)

