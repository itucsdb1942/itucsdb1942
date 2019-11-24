import os
import sys
import psycopg2 as dbapi2
import dbinit as db

url=db.url

book_data = [
    {'title': "Harry Potter and the Philosopher's Stone",
     'writer': "J. K. Rowling",
     'year_pub': 2014,
     'tpage': 352,
     'publisher':"Bloomsbury",
     'language': "English",
     'genre':"Fantastic",
     'score': 8,
     'vote': 5},

     {'title': "Homo Deus",
     'writer':  "Yuval Noah Harari",
     'year_pub': 2017,
     'tpage': 528,
     'publisher':"Vintage",
     'language': "English",
     'genre':"Science",
     'score': 9,
     'vote': 6},

     {'title': "İnce Memed1",
     'writer': "Yaşar Kemal",
     'year_pub': 8.7,
     'tpage': 35027,
     'publisher':"yapı kredi",
     'language': "türkçe",
     'genre':"Novel",
     'score': 10,
     'vote': 8},

     {'title': "Game of Thrones",
     'writer': "George R. R. Martin",
     'year_pub': 8.7,
     'tpage': 4272,
     'publisher':"hbo",
     'language': "English",
     'genre':"Fantastic",
     'score': 9,
     'vote': 10},

     {'title': "Gece",
     'writer': "Bilge Karasu",
     'year_pub': 1990,
     'tpage': 232,
     'publisher':"Metis",
     'language': "Türkçe",
     'genre':"Novel",
     'score': 10,
     'vote': 15},
]




writer_ids = {}
try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
            for item in book_data:
                wri_names = [item['writer']]
                for name in wri_names:
                    if name not in writer_ids:
                        statement = """INSERT INTO writer (wr_name) VALUES (%s)
                                    RETURNING id;"""
                    
                        cursor.execute(statement,(name,))
                        connection.commit()
                        writer_id = cursor.fetchone()[0]
                        writer_ids[name] = writer_id       
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()

writer_book = {}
with dbapi2.connect(url) as connection:
    with connection.cursor() as cursor:
        statement = """SELECT id, wr_name FROM writer; """
        cursor.execute(statement)
        for id, name in cursor:
            writer_book[name] = id
connection.close()

try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
            for item in book_data:
                statement = """INSERT INTO books (NAME, WRITERID, PUB_YEAR, T_PAGE, PUBLISHER, LANGUAGE, GENRE, SCORE, VOTE)
                            VALUES (%(title)s, %(writerid)s, %(year_pub)s, %(tpage)s,
                                    %(publisher)s, %(language)s, %(genre)s, %(score)s, %(vote)s)
                    RETURNING id;"""
                item['writerid'] = writer_book[item['writer']]
                
                cursor.execute(statement,item)
                connection.commit()
                book_id = cursor.fetchone()[0]
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()

