import os
import sys

import psycopg2 as dbapi2


url="postgres://dneperyi:l94XrLU-lOV2MOaQOPBnoYqVdKreucNZ@manny.db.elephantsql.com:5432/dneperyi"
INIT_STATEMENTS = [
    """SELECT * FROM tvseries;
    """
   
]

#dsn = """user='postgres' password='docker'
 #       host='localhost' port=5432 dbname='mydatabase'"""


def initialize(url):
    try:
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        statement = """CREATE DOMAIN SCORES AS FLOAT
            CHECK((VALUE>=1.0) AND (VALUE<=10.0));
        
        """
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()


    try:
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        statement = """
            CREATE TABLE tvseries (
            ID SERIAL PRIMARY KEY,
            TITLE VARCHAR(80) UNIQUE NOT NULL,
            CHANNEL VARCHAR(80),
            LANGUAGE VARCHAR(80),
            SEASON INTEGER,
            YEAR INTEGER,
            GENRE VARCHAR(80),
            VOTE INTEGER,
            SCORE SCORES
        );"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()

    try:
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        statement = """ CREATE TABLE books(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(80),
            WRITER VARCHAR(80),
            PUB_YEAR INTEGER,
            T_PAGE INTEGER,
            PUBLISHER VARCHAR(80),
            LANGUAGE VARCHAR(80),
            GENRE VARCHAR(80),
            SCORE SCORES,
            VOTE INTEGER); """
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()

    
"""  with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
            for row in cursor:
                idd, title, ep = row
                printf.name = title
                printf.idd = idd
                printf.ep = ep

                
        cursor.close()"""
        


if __name__ == "__main__":
    print(44)
else:
    initialize(url)

