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

    def com_like_numberb(self):
            statement = """ SELECT likeb FROM comment_b
                        WHERE id = %s;"""
            cursor.execute(statement, (  self.id,))
            like_n=cursor.fetchone()[0]
            connection.commit()
            return like_n

    def com_dislike_numberb(self):
                statement = """ SELECT dislikeb FROM comment_b
                            WHERE  id = %s;"""
                cursor.execute(statement, (  self.id,))
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
                check=cursor.fetchone()[0]
                if check == False:
                    a="TRUE"
                statement = """ UPDATE book_list 
                            SET fav_b = %s WHERE userid = %s AND bookid = %s"""
                cursor.execute(statement, (a, userid, bookid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            connection.rollback()
            cursor=connection.cursor()

def hate_addb(userid,bookid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO book_list (userid, bookid, hate_b)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,bookid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            
            a="FALSE"
            with connection.cursor() as cursor:    
                statement = """ SELECT hate_b FROM book_list
                            WHERE userid = %s AND bookid = %s;"""
                cursor.execute(statement, ( userid, bookid,))
                check=cursor.fetchone()[0]
                if check == False:
                    a="TRUE"
                statement = """ UPDATE book_list 
                            SET hate_b = %s WHERE userid = %s AND bookid = %s"""
                cursor.execute(statement, (a, userid, bookid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            connection.rollback()
            cursor=connection.cursor()

def wish_addb(userid,bookid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO book_list (userid, bookid, wish_b)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,bookid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            
            a="FALSE"
            with connection.cursor() as cursor:    
                statement = """ SELECT wish_b FROM book_list
                            WHERE userid = %s AND bookid = %s;"""
                cursor.execute(statement, ( userid, bookid,))
                check=cursor.fetchone()[0]
                if check == False:
                    a="TRUE"
                statement = """ UPDATE book_list 
                            SET wish_b = %s WHERE userid = %s AND bookid = %s;"""
                cursor.execute(statement, (a, userid, bookid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            connection.rollback()
            cursor=connection.cursor()
            
def add_score(bookid,score):
    with connection.cursor() as cursor:
        statement = """ UPDATE books
                                SET SCORE = (SCORE*VOTE+%s)/(VOTE+1),VOTE=VOTE+1 WHERE id = %s;"""
        cursor.execute(statement, (score, bookid,))
        connection.commit()   
        cursor.close()  

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
                        connection.rollback()
                        cursor=connection.cursor()
                        checkreaded=0
                        statement="""SELECT readpage FROM book_trace WHERE bookid= (%s) AND userid=(%s)"""
                        cursor.execute(statement,(self.id,userid,))
                        for p in cursor:
                            checkreaded=p
                        if(checkreaded == 0):
                            return 0
                        connection.commit()
                        per=checkreaded[0]
                        percent=per*100/self.tpage
                        if(percent==100.0):
                            readed_add(userid,self.id)
                        elif(percent>0.0):
                            reading_add(userid,self.id)
                        elif(percent==0.0):
                            notread_add(userid,self.id)
                        return round(percent,2)

    def page_readed(self,userid):
                        with connection.cursor() as cursor:
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
                connection.rollback()
                try:
                    with connection.cursor() as cursor:
                        statement = """ SELECT fav_b FROM book_list
                                    WHERE userid = %s AND bookid = %s;"""
                        cursor.execute(statement, ( userid, self.id,))
                        connection.commit()
                        check=cursor.fetchone()[0]
                        if check==False:
                            return False
                        return True
                except:
                    return False
    def check_hate(self,userid):
                connection.rollback()
                try:
                    with connection.cursor() as cursor:
                        statement = """ SELECT hate_b FROM book_list
                                    WHERE userid = %s AND bookid = %s;"""
                        cursor.execute(statement, ( userid, self.id,))
                        connection.commit()
                        check=cursor.fetchone()[0]
                        if check==False:
                            return False
                        return True
                except:
                    return False
    def check_wish(self,userid):
                connection.rollback()
                try:
                    with connection.cursor() as cursor:
                        statement = """ SELECT wish_b FROM book_list
                                    WHERE userid = %s AND bookid = %s;"""
                        cursor.execute(statement, ( userid, self.id,))
                        connection.commit()
                        check=cursor.fetchone()[0]
                        if check==False:
                            return False
                        return True
                except:
                    return False

def readed_add(userid, bookid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO book_list (userid, bookid, readed)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,bookid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            with connection.cursor() as cursor:    
                statement = """ UPDATE book_list 
                            SET readed = %s,  reading = %s WHERE userid = %s AND bookid = %s;"""
                cursor.execute(statement, ("TRUE","FALSE", userid, bookid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            connection.rollback()
            cursor=connection.cursor()          

def reading_add(userid, bookid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO book_list (userid, bookid, reading)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,bookid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            with connection.cursor() as cursor:    
                statement = """ UPDATE book_list 
                            SET readed = %s,  reading = %s WHERE userid = %s AND bookid = %s;"""
                cursor.execute(statement, ("FALSE","TRUE", userid, bookid,))
                connection.commit()

def notread_add(userid, bookid):
        try:
            with connection.cursor() as cursor:    
                statement = """ UPDATE book_list 
                            SET readed = %s,  reading = %s WHERE userid = %s AND bookid = %s;"""
                cursor.execute(statement, ("FALSE","FALSE", userid, bookid,))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            

def submit_commit_book(bookid,userid,header,context):
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
            

def print_commit_book(bookid):
            commits=[]
            try:
                with connection.cursor() as cursor:
                                statement = """SELECT comment_b.id, comment_b.headerb,comment_b.contentb,comment_b.date, users.username FROM comment_b,users
                                             WHERE comment_b.userid=users.id ORDER BY date DESC;"""                
                                cursor.execute(statement,)
                                for id,head,cont,date,username in cursor:
                                    com=commitb(id=id, username=username,bookid=bookid,header=head,content=cont,date=date)
                                    commits.append(com)  
                                
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
                  
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
    
def  delete_commitb(idno, userid):
    try:
        with connection.cursor() as cursor:
                    statement = """ DELETE FROM comment_b 
                                WHERE userid = %s AND id = %s"""
                    cursor.execute(statement, ( userid, idno,))
                    connection.commit()
    except:
        connection.rollback()
        cursor=connection.cursor()
    
def print_book():
                with connection.cursor() as cursor:
                    book_list=[]
                    statement = """SELECT books.ID, books.NAME, writer.wr_name, books.PUB_YEAR, books.T_PAGE, books.PUBLISHER, 
                    books.LANGUAGE, books.GENRE, books.SCORE, books.VOTE FROM BOOKS, writer WHERE books.writerid=writer.id ORDER BY id; """
                    cursor.execute(statement)
                    for id, name, wr_name, year, page, pub, lang, gen, sc, vote in cursor:
                            book =Book(id,name,wr_name,year,page,gen,pub,lang,vote,sc)
                            book_list.append(book)
                    connection.commit()
                    return book_list
def print_book_by_az():
                with connection.cursor() as cursor:
                    book_list=[]
                    statement = """SELECT books.ID, books.NAME, writer.wr_name, books.PUB_YEAR, books.T_PAGE, books.PUBLISHER, 
                    books.LANGUAGE, books.GENRE, books.SCORE, books.VOTE FROM BOOKS, writer WHERE books.writerid=writer.id ORDER BY books.name; """
                    cursor.execute(statement)
                    for id, name, wr_name, year, page, pub, lang, gen, sc, vote in cursor:
                            book =Book(id,name,wr_name,year,page,gen,pub,lang,vote,sc)
                            book_list.append(book)
                    connection.commit()
                    return book_list
def print_book_by_score():
                with connection.cursor() as cursor:
                    book_list=[]
                    statement = """SELECT books.ID, books.NAME, writer.wr_name, books.PUB_YEAR, books.T_PAGE, books.PUBLISHER, 
                    books.LANGUAGE, books.GENRE, books.SCORE, books.VOTE FROM BOOKS, writer WHERE books.writerid=writer.id ORDER BY books.score DESC; """
                    cursor.execute(statement)
                    for id, name, wr_name, year, page, pub, lang, gen, sc, vote in cursor:
                            book =Book(id,name,wr_name,year,page,gen,pub,lang,vote,sc)
                            book_list.append(book)
                    connection.commit()
                    return book_list                    
def print_book_by_year():
                with connection.cursor() as cursor:
                    book_list=[]
                    statement = """SELECT books.ID, books.NAME, writer.wr_name, books.PUB_YEAR, books.T_PAGE, books.PUBLISHER, 
                    books.LANGUAGE, books.GENRE, books.SCORE, books.VOTE FROM BOOKS, writer WHERE books.writerid=writer.id ORDER BY books.pub_year DESC; """
                    cursor.execute(statement)
                    for id, name, wr_name, year, page, pub, lang, gen, sc, vote in cursor:
                            book =Book(id,name,wr_name,year,page,gen,pub,lang,vote,sc)
                            book_list.append(book)
                    connection.commit()
                    return book_list
def find_book(idno):
        
                statement = """SELECT books.ID, books.NAME, writer.wr_name, books.PUB_YEAR, books.T_PAGE, books.PUBLISHER, 
                books.LANGUAGE, books.GENRE, books.SCORE, books.VOTE FROM BOOKS, writer WHERE books.id=%s AND books.writerid=writer.id; """
                cursor.execute(statement,(idno,))
                connection.commit()
                for id, name, wri_name, year, page, pub, lang, gen, sc, vote in cursor:
                    book =Book(id,name,wri_name,year,page,gen,pub,lang,vote,sc)
                return book

def print_reading(idno):
    books={}
    try:
        with connection.cursor() as cursor:
                                statement = """SELECT book_list.bookid, books.name FROM book_list,books
                                             WHERE book_list.reading=TRUE AND book_list.bookid=books.id AND userid=%s;"""                
                                cursor.execute(statement,(idno,))
                                for bookid, bookname in cursor:
                                    books[bookid]=bookname
                                return books
    except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
def print_readed(idno):
    books={}
    try:
        with connection.cursor() as cursor:
                                statement = """SELECT book_list.bookid, books.name FROM book_list,books
                                             WHERE book_list.readed=TRUE AND book_list.bookid=books.id AND userid=%s;"""                
                                cursor.execute(statement,(idno,))
                                for bookid, bookname in cursor:
                                    books[bookid]=bookname
                                return books
    except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()          

def print_wishb(idno):
    books={}
    try:
        with connection.cursor() as cursor:
                                statement = """SELECT book_list.bookid, books.name FROM book_list,books
                                             WHERE book_list.wish_b=TRUE AND book_list.bookid=books.id AND userid=%s;"""                
                                cursor.execute(statement,(idno,))
                                for bookid, bookname in cursor:
                                    books[bookid]=bookname
                                return books
    except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()       
def print_favb(idno):
    books={}
    try:
        with connection.cursor() as cursor:
                                statement = """SELECT book_list.bookid, books.name FROM book_list,books
                                             WHERE book_list.fav_b=TRUE AND book_list.bookid=books.id AND userid=%s;"""                
                                cursor.execute(statement,(idno,))
                                for bookid, bookname in cursor:
                                    books[bookid]=bookname
                                return books
    except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()       
def print_hateb(idno):
    books={}
    try:
        with connection.cursor() as cursor:
                                statement = """SELECT book_list.bookid, books.name FROM book_list,books
                                             WHERE book_list.hate_b=TRUE AND book_list.bookid=books.id AND userid=%s;"""                
                                cursor.execute(statement,(idno,))
                                for bookid, bookname in cursor:
                                    books[bookid]=bookname
                                return books
    except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()           
def initial_book():
                book_data = [
                    {'title': "Harry Potter and the Philosopher's Stone",
                    'writer': "J. K. Rowling",
                    'year_pub': 2014,
                    'tpage': 352,
                    'publisher':"Bloomsbury",
                    'language': "English",
                    'genre':"Fantastic"},

                    {'title': "Homo Deus",
                    'writer':  "Yuval Noah Harari",
                    'year_pub': 2017,
                    'tpage': 528,
                    'publisher':"Vintage",
                    'language': "English",
                    'genre':"Science"},

                    {'title': "İnce Memed1",
                    'writer': "Yaşar Kemal",
                    'year_pub': 8.7,
                    'tpage': 35027,
                    'publisher':"yapı kredi",
                    'language': "türkçe",
                    'genre':"Novel"},

                    {'title': "Game of Thrones",
                    'writer': "George R. R. Martin",
                    'year_pub': 8.7,
                    'tpage': 4272,
                    'publisher':"hbo",
                    'language': "English",
                    'genre':"Fantastic"},

                    {'title': "Gece",
                    'writer': "Bilge Karasu",
                    'year_pub': 1990,
                    'tpage': 232,
                    'publisher':"Metis",
                    'language': "Türkçe",
                    'genre':"Novel"},
                ]

                cursor=connection.cursor()
                writer_ids = {}
                try:
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
                except:
                    connection.rollback()

                with connection.cursor() as cursor:
                    writer_book = {}
                    statement = """SELECT id, wr_name FROM writer; """
                    cursor.execute(statement,)
                    for id, name in cursor:
                        writer_book[name] = id
                    connection.commit()

    
                for item in book_data:
                    with connection.cursor() as cursor:
                        statement = """INSERT INTO books (NAME, WRITERID, PUB_YEAR, T_PAGE, PUBLISHER, LANGUAGE, GENRE)
                                    VALUES (%s, %s, %s, %s,
                                            %s, %s, %s)
                            RETURNING id;"""
                        item['writerid'] = writer_book[item['writer']]
                        
                        cursor.execute(statement,(item['title'],item['writerid'],item['year_pub'],item['tpage'],item['publisher'],item['language'],item['genre'],))
                        connection.commit()
                        book_id = cursor.fetchone()[0]
                        cursor.close()
    


