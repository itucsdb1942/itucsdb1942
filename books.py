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



publisher_ids ={}
try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
             for item in book_data:
                pub_names = [item['publisher']]
                for name in pub_names:
                    if name not in publisher_ids:
                        statement = """INSERT INTO publisher (pub_name) VALUES (%s)
                                    RETURNING id"""
                        cursor.execute(statement, (name,))
                        connection.commit()
                        pub_id = cursor.fetchone()[0]
                        publisher_ids[name] = pub_id       
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()

publisher_book = {}
with dbapi2.connect(url) as connection:
    with connection.cursor() as cursor:
        statement = """SELECT id, pub_name FROM publisher; """
        cursor.execute(statement)
        for id, name in cursor:
            publisher_book[name] = id
connection.close()
print(publisher_book)


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
print(writer_book)

genre_ids = {}
try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
            for item in book_data:
                genre_names = [item['genre']]
                
                for name in genre_names:
                    if name not in genre_ids:
                        statement = """INSERT INTO genre (genre_name) VALUES (%s)
                                    RETURNING id"""
                        cursor.execute(statement, (name,))
                        connection.commit()
                        genre_id = cursor.fetchone()[0]
                        genre_ids[name] = genre_id
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()

genre_book={}
with dbapi2.connect(url) as connection:
    with connection.cursor() as cursor:
            statement = """SELECT id, genre_name FROM genre; """
            cursor.execute(statement)
            for id, name in cursor:
                genre_book[name]= id
connection.close()
print(genre_book)


try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
            for item in book_data:
                statement = """INSERT INTO books (NAME, WRITERID, PUB_YEAR, T_PAGE, PUBLISHERID, LANGUAGE, GENREID, SCORE, VOTE)
                            VALUES (%(title)s, %(writerid)s, %(year_pub)s, %(tpage)s,
                                    %(publisherid)s, %(language)s, %(genreid)s, %(score)s, %(vote)s)
                    RETURNING id;"""
                item['publisherid'] = publisher_book[item['publisher']]
                item['genreid'] = genre_book[item['genre']]
                item['writerid'] = writer_book[item['writer']]
                
                cursor.execute(statement,item)
                connection.commit()
                book_id = cursor.fetchone()[0]
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()

