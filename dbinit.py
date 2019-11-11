import os
import sys

import psycopg2 as dbapi2

url="postgres://dneperyi:l94XrLU-lOV2MOaQOPBnoYqVdKreucNZ@manny.db.elephantsql.com:5432/dneperyi"

INIT_STATEMENTS = [

    """ CREATE DOMAIN SCORES AS FLOAT
            CHECK((VALUE>=0.0) AND (VALUE<=10.0)) DEFAULT 0.0;""",

    """ CREATE TABLE user (
            ID SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            surname VARCHAR(20) NOT NULL,
            username VARCHAR(20) UNIQUE NOT NULL,
            email VARCHAR(40) NOT NULL,
            gender VARCHAR(6) NOT NULL,
            date DATE NOT NULL,
            password VARCHAR(40) NOT NULL
        );""",

        """CREATE TABLE channel( 
                ID SERIAL PRIMARY KEY,
                chan_name  VARCHAR(40) UNIQUE
        );""",

        """CREATE TABLE tvseries (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(80) UNIQUE NOT NULL,
            CHANNELID INTEGER REFERENCES channel(id),
            LANGUAGE VARCHAR(20),
            SEASON INTEGER,
            YEAR INTEGER,
            GENRE VARCHAR(20),
            VOTE INTEGER DEFAULT 0,
            SCORE SCORES
        );""",

        """ CREATE TABLE episode (
            ID SERIAL PRIMARY KEY,
            TVID INTEGER REFERENCES tvseries(id),
            season_n INTEGER,
            number INTEGER,
            name VARCHAR(80)
        );""",

       """ CREATE TABLE season (
            TVID INTEGER REFERENCES tvseries(id),
            EPID INTEGER REFERENCES episode(id),
            episode_no INTEGER,
            PRIMARY KEY(TVID,EPID)
        );""",


         """CREATE TABLE publisher( 
                ID SERIAL PRIMARY KEY,
                pub_name  VARCHAR(40) UNIQUE,
                pub_country VARCHAR(40)
        );""",

        """CREATE TABLE writer(
            ID SERIAL PRIMARY KEY,
            wr_name VARCHAR(50) NOT NULL UNIQUE,
            wr_country VARCHAR(50)
        );""",

        """CREATE TABLE genre(
            ID SERIAL PRIMARY KEY,
            genre_name VARCHAR(50) UNIQUE
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

       """ CREATE TABLE users(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(20) NOT NULL,
            SURNAME VARCHAR(20) NOT NULL,
            USERNAME VARCHAR(20) UNIQUE NOT NULL,
            mail VARCHAR(80) UNIQUE NOT NULL,
            gender VARCHAR(6) NOT NULL,
            birth DATE NOT NULL,
            password VARCHAR(80) NOT NULL
            );""",

    
]

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

initialize(url)





