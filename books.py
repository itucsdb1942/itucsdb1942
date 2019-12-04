import os
import sys
import psycopg2 as dbapi2
import dbinit as db

connection = db.con(db.url)
class Book:
    def __init__(self, id=None, name=None, writer=None,year_pub=None,tpage=None,genre=None,publisher=None, language=None,vote=None,score= None):
        self.id = id
        self.name= name
        self.writer= writer
        self.year_pub= year_pub
        self.tpage= tpage
        self.genre= genre
        self.publisher= publisher 
        self.language= language 
        self.vote=vote 
        self.score=score

    def addbook(self):
        writer_ids={}
        try:
            with connection.cursor() as cursor:
                wri_name = self.writer
                statement = """SELECT id FROM writer WHERE wr_name= (%s);"""
                cursor.execute(statement,(wri_name,))
                connection.commit()
                writer_id = cursor.fetchone()[0]   
                writer_ids[wri_name]=writer_id
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            cursor.close()

        try:
            with connection.cursor() as cursor:
                wri_name = self.writer
                statement = """INSERT INTO writer (wr_name) VALUES (%s)
                                        RETURNING id;"""
                        
                cursor.execute(statement,(wri_name,))
                connection.commit()
                writer_id = cursor.fetchone()[0]   
                writer_ids[wri_name]=writer_id
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            cursor.close()

        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO books (NAME, WRITERID, PUB_YEAR, T_PAGE, PUBLISHER, LANGUAGE, GENRE, SCORE, VOTE)
                                    VALUES (%s,%s,%s, %s,%s,%s,%s,%s,%s)
                            RETURNING id;"""
                cursor.execute(statement, (self.name, writer_ids[self.writer], self.year_pub, self.tpage, self.publisher, self.language, self.genre, self.score, self.vote))
                connection.commit()
                book_id = cursor.fetchone()[0]
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            cursor.close()

    

def print_book():
        book_list=[]
        with connection.cursor() as cursor:
                statement = """SELECT NAME, WRITERID, PUB_YEAR, T_PAGE, PUBLISHER, LANGUAGE, GENRE, SCORE, VOTE FROM BOOKS; """
                cursor.execute(statement)
                for id, name, wri_id, year, page, pub, lang, gen, sc, vote in cursor:
                            statement = """SELECT WR_NAME FROM  writer WHERE id=%s; """
                            cursor.execute(statement,(wri_id,))
                            wr_name =cursor.fetchone()[0]     
                   
                book =Book(id, name,wr_name, year, page, pub, lang, gen, sc, vote)
                book_list.append(book)
        cursor.close()
        return book_list

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
    cursor.close()

writer_book = {}
with connection.cursor() as cursor:
        statement = """SELECT id, wr_name FROM writer; """
        cursor.execute(statement)
        for id, name in cursor:
            writer_book[name] = id
cursor.close()

try:
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
    cursor.close()

