import os
import sys
import psycopg2 as dbapi2
import dbinit as db
from datetime import datetime

connection = db.connection
cursor=connection.cursor()

class commitb:
    def __init__(self,id=0,username=0,bookid=0,header=0,content=0,date=0,like=0,dislike=0):
        self.id=id
        self.username=username
        self.bookid=bookid
        self.header=header
        self.content=content
        self.date=date
        self.like=like
        self.dislike=dislike

    def com_like_numberb(self,userid):
            statement = """ SELECT likeb FROM comment_b
                        WHERE userid = %s AND id = %s;"""
            cursor.execute(statement, ( userid, self.id,))
            like_n=cursor.fetchone()[0]
            connection.commit()
            return like_n

    def com_dislike_numberb(self,userid):
                statement = """ SELECT dislikeb FROM comment_b
                            WHERE userid = %s AND id = %s;"""
                cursor.execute(statement, ( userid, self.id,))
                dislike_n=cursor.fetchone()[0]
                connection.commit()
                return dislike_n

def com_like_book(commitid):
            statement = """ UPDATE comment_b
                        SET likeb= likeb+1 WHERE id = %s;"""
            cursor.execute(statement, ( commitid,))
            connection.commit()
        

def com_dislike_book(commitid):
            statement = """ UPDATE comment_b
                        SET dislikeb = dislikeb + 1 WHERE id = %s;"""
            cursor.execute(statement, (  commitid,))
            connection.commit()

def fav_addb(userid,bookid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO book_list (userid, bookid, fav_b)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,bookid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            
            a="FALSE"
            with connection.cursor() as cursor:    
                statement = """ SELECT fav_b FROM book_list
                            WHERE userid = %s AND bookid = %s;"""
                cursor.execute(statement, ( userid, bookid,))
                print("except")
                check=cursor.fetchone()[0]
                print("ddd")
                if check == False:
                    a="TRUE"
                statement = """ UPDATE book_list 
                            SET fav_b = %s WHERE userid = %s AND bookid = %s"""
                cursor.execute(statement, (a, userid, bookid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            print("hata")
            connection.rollback()
            cursor=connection.cursor()


            
            
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
            cursor=connection.cursor()
        

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
            cursor=connection.cursor()
        

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
            cursor=connection.cursor()
        
    def book_percent(self,userid):
                        checkreaded=0
                        statement="""SELECT readpage FROM book_trace WHERE bookid= (%s) AND userid=(%s)"""
                        cursor.execute(statement,(self.id,userid,))
                        for p in cursor:
                            checkreaded=p
                        if(checkreaded == 0):
                            return 0
                        connection.commit()
                        per=checkreaded[0]
                        print(per,self.tpage)
                        return int(per*100/self.tpage)

    def page_readed(self,userid):
                        checkreaded=0
                
                        statement="""SELECT readpage FROM book_trace WHERE bookid= (%s) AND userid=(%s)"""
                        cursor.execute(statement,(self.id,userid,))
                        for p in cursor:
                            checkreaded=p
                        if(checkreaded == 0):
                            return 0
                        connection.commit()
                        per=checkreaded[0]
                        return per

    def check_fav(self,userid):
                a=0
                connection.rollback()
                with connection.cursor() as cursor:
                    statement = """ SELECT fav_b FROM book_list
                                WHERE userid = %s AND bookid = %s;"""
                    cursor.execute(statement, ( userid, self.id,))
                    connection.commit()
                    for check in cursor:
                        a=check
                    if a[0]==False:
                        return False
                    return True

def submit_commit_book(bookid,userid,header,context):
            print("fksdf")
            now = datetime.now()
            try:
                with connection.cursor() as cursor:
                                statement = """INSERT INTO comment_b (userid, bookid, headerb, contentb,date)
                                            VALUES (%s, %s, %s, %s, %s)
                                        RETURNING id;"""                
                                cursor.execute(statement,(userid,bookid,header,context,now))
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
            

def print_commit_book(bookid,userid):
            commits=[]
            try:
                with connection.cursor() as cursor:
                                statement = """SELECT username FROM users
                                             WHERE id=(%s);"""                
                                cursor.execute(statement,(userid,))
                                username=cursor.fetchone()[0]
                                connection.commit()
                                statement = """SELECT id, headerb,contentb,date FROM comment_b
                                             WHERE userid=(%s) AND bookid=(%s) ORDER BY date DESC;"""                
                                cursor.execute(statement,(userid,bookid))
                                for id,head,cont,date in cursor:
                                    com=commitb(id=id,username=username,bookid=bookid,header=head,content=cont,date=date)
                                    commits.append(com)    
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
           
            print(commits)
            return commits


def check_tpage(readed,bookid,userid):
                
                        statement="""SELECT t_page FROM books WHERE id= (%s)"""
                        cursor.execute(statement,(bookid,))
                        tpage=cursor.fetchone()[0] 
                        connection.commit() 
                        if readed>tpage:
                            return False
                        return True
     
def updatepage(bookid, userid, page):
    
    try:
        with connection.cursor() as cursor:
            statement = """INSERT INTO book_trace (userid, bookid, readpage)
                        VALUES ( %s, %s, %s)
                    RETURNING id;"""
            cursor.execute(statement,(userid,bookid,page,))
            connection.commit()
    except dbapi2.errors.UniqueViolation:
        connection.rollback()
        with connection.cursor() as cursor:
            statement = """ UPDATE book_trace 
                        SET readpage = %s WHERE userid = %s AND bookid = %s"""
            cursor.execute(statement, (page, userid, bookid,))
            connection.commit()
    except dbapi2.errors.InFailedSqlTransactions:
        connection.rollback()
        cursor=connection.cursor()
    
    
  
    
def print_book():
                book_list=[]
                statement = """SELECT ID, NAME, WRITERID, PUB_YEAR, T_PAGE, PUBLISHER, LANGUAGE, GENRE, SCORE, VOTE FROM BOOKS; """
                cursor.execute(statement)
                for id, name, wri_id, year, page, pub, lang, gen, sc, vote in cursor:
                        with connection.cursor() as cursor2:
                            statement = """SELECT WR_NAME FROM  writer WHERE id=%s; """
                            cursor2.execute(statement,(wri_id,))
                            wr_name =cursor2.fetchone()[0]     
                        book =Book(id, name, wr_name, year, page, pub, lang, gen, sc, vote)
                        book_list.append(book)
                connection.commit()
                return book_list

def find_book(idno):
        
                statement = """SELECT ID, NAME, WRITERID, PUB_YEAR, T_PAGE, PUBLISHER, LANGUAGE, GENRE, SCORE, VOTE FROM BOOKS WHERE id=%s; """
                cursor.execute(statement,(idno,))
                connection.commit()
                for id, name, wri_id, year, page, pub, lang, gen, sc, vote in cursor:
                    statement = """SELECT WR_NAME FROM  writer WHERE id=%s; """
                    cursor.execute(statement,(wri_id,))
                    wr_name =cursor.fetchone()[0]  
                    connection.commit() 
                book = Book(id, name, wr_name, year, page, pub, lang, gen, sc, vote)
        
                return book


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
    cursor=connection.cursor()


writer_book = {}
statement = """SELECT id, wr_name FROM writer; """
cursor.execute(statement)
for id, name in cursor:
    writer_book[name] = id
connection.commit()

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
    cursor=connection.cursor()


