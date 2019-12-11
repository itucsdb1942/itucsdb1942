import os
import sys
import psycopg2 as dbapi2

url="postgres://dneperyi:l94XrLU-lOV2MOaQOPBnoYqVdKreucNZ@manny.db.elephantsql.com:5432/dneperyi"

INIT_STATEMENTS = [

    """ CREATE DOMAIN SCORES AS FLOAT
            CHECK((VALUE>=0.0) AND (VALUE<=10.0)) DEFAULT 0.0;""",

        """ CREATE TABLE users(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(20) NOT NULL,
            SURNAME VARCHAR(20) NOT NULL,
            USERNAME VARCHAR(20) UNIQUEUNI NOT NULL,
            mail VARCHAR(80) UNIQUE NOT NULL,
            gender VARCHAR(6) NOT NULL,
            birth DATE NOT NULL,
            password VARCHAR(80) NOT NULL
            );""",

        """CREATE TABLE tvseries (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(80) UNIQUE NOT NULL,
            CHANNEL VARCHAR(20),
            LANGUAGE VARCHAR(20),
            SEASON INTEGER,
            YEAR INTEGER,
            GENRE VARCHAR(20),
            VOTE INTEGER DEFAULT 0,
            SCORE SCORES
        );""",

         """ CREATE TABLE tv_commit(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id),
            tvid INTEGER REFERENCES tvseries(id),
            header VARCHAR(20),
            content VARCHAR(200),
            LIKE_N INTEGER DEFAULT 0,
            DISLIKE_N INTEGER DEFAULT 0,
            date DATE
            );""", 

        """ CREATE TABLE episode (
            ID SERIAL PRIMARY KEY,
            tvid INTEGER REFERENCES tvseries(id),
            season_n INTEGER,
            number INTEGER,
            name VARCHAR(80),
            year INTEGER,
            VOTE INTEGER DEFAULT 0,
            SCORE SCORES,
            UNIQUE(tvid,season_n,number)
        );""",

    """ CREATE TABLE tv_list(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id),
            tvid INTEGER REFERENCES tvseries(id),
            fav_list BOOL DEFAULT FALSE,
            wish_list BOOL DEFAULT FALSE,
            watched_list BOOL DEFAULT FALSE,
            watching_list BOOL DEFAULT FALSE
            );""",

     """ CREATE TABLE tv_trace(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id),
            episodeid INTEGER REFERENCES episode(id),
            watched BOOL DEFAULT FALSE
            );""",

       """CREATE TABLE writer(
            ID SERIAL PRIMARY KEY,
            wr_name VARCHAR(50) NOT NULL UNIQUE,
            wr_country VARCHAR(50)
        );""",

         """ CREATE TABLE books(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(80) UNIQUE NOT NULL,
            WRITERID INTEGER REFERENCES writer(id),
            PUB_YEAR INTEGER,
            T_PAGE INTEGER,
            PUBLISHER VARCHAR(50),
            LANGUAGE VARCHAR(80),
            GENRE VARCHAR(50),
            SCORE SCORES DEFAULT 0,
            VOTE INTEGER DEFAULT 0);""",

        """CREATE TABLE collbook(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id),
            bookid INTEGER REFERENCES books(id),
            coll_name VARCHAR(50) NOT NULL,
            numberofbook INTEGER DEFAULT 0,
            like INTEGER DEFAULT 0,
            dislike INTEGER DEFAULT 0,
            date DATE,
            UNIQUE(userid, coll_name)
        );""",

        """CREATE TABLE book_list(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id),
            bookid INTEGER REFERENCES books(id),
            fav_b BOOL DEFAULT FALSE,
            wish_b BOOL DEFAULT FALSE,
            readed BOOL DEFAULT FALSE,
            reading BOOL DEFAULT FALSE,
            collid INTEGER REFERENCES collbook(id)
        );""",

        """CREATE TABLE book_trace(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id),
            bookid INTEGER REFERENCES books(id),
            readpage INTEGER DEFAULT 0,
            UNIQUE(userid, bookid)
        );""",

        """CREATE TABLE comment_b(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id),
            bookid INTEGER REFERENCES books(id),
            headerb VARCHAR(30),
            contentb VARCHAR(250),
            like INTEGER DEFAULT 0,
            dislike INTEGER DEFAULT 0,
            date DATE
        );"""
 
]
connection = dbapi2.connect(url)


def initialize(url):
    for statement in INIT_STATEMENTS:
        try:
            cursor = connection.cursor()
            cursor.execute(statement)
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()

initialize(url)





