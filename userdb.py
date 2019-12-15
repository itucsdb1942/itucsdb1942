import os
import sys
import psycopg2 as dbapi2
import dbinit as db
from flask_login import UserMixin
connection=db.connection

class User(UserMixin):
    def __init__(self, id = None, name = None ,surname = None ,username = None ,mail = None ,gender = None ,date = None ,password = None):
        self.id=id
        self.name=name
        self.surname=surname
        self.username=username
        self.mail=mail
        self.gender=gender
        self.date=date
        self.password=password

    def adduser(self):

        user_data =  {'name': self.name,
                        'surname': self.surname,
                        'username': self.username,
                        'mail': self.mail,
                        'gender': self.gender,
                        'birth': self.date,
                        'password': self.password}
      

        try:
                with connection.cursor() as cursor:
                            statement = """INSERT INTO users (name, surname, username, mail, gender, birth, password)
                                        VALUES (%(name)s, %(surname)s, %(username)s, %(mail)s, %(gender)s, %(birth)s, %(password)s)
                                    RETURNING id;"""       
                            cursor.execute(statement,user_data)
                            connection.commit()
                            user_id = cursor.fetchone()[0]
        except dbapi2.DatabaseError:
            connection.rollback() 
        

    
def get(user_id):
            with connection.cursor() as cursor:
                    statement = """SELECT id, name, surname, username, mail, gender, birth, password FROM users 
                                        WHERE id = ({}); """.format(user_id)
                    cursor.execute(statement)
                    user= False
                    for i, n, s, u, m, g, b, p  in cursor:
                        user= User(id=i, name=n, surname=s, username=u,
                        mail=m, gender=g, date=b, password=p)
                    return user
            

def username_check(username):
            with connection.cursor() as cursor:
                    statement = """SELECT id, name, surname, username, mail, gender, birth, password FROM users 
                                        WHERE username = (%s); """
                    cursor.execute(statement,(username,))
                    print("kdfkd")
                    user= False
                    for i, n, s, u, m, g, b, p  in cursor:
                        user= User(id=i, name=n, surname=s, username=u,
                        mail=m, gender=g, date=b, password=p)
                    return user
            
    
def mail_check(mail):
            with connection.cursor() as cursor:
                    statement = """SELECT id, name, surname, username, mail, gender, birth, password FROM users 
                                        WHERE mail = (%s); """
                    cursor.execute(statement,(mail,))
                    user= False
                    for i, n, s, u, m, g, b, p  in cursor:
                        user= User(id=i, name=n, surname=s, username=u,
                        mail=m, gender=g, date=b, password=p)
                    return user
            
def update_user(username,mail,id):
    with connection.cursor() as cursor:
                    statement = """UPDATE users SET mail = (%s), username=(%s) WHERE id=(%s); """
                    cursor.execute(statement,(mail,username,id))
                    
def delete_user(idno):
    with connection.cursor() as cursor:
                    statement = """DELETE FROM tv_list WHERE userid=(%s) ;
                                    DELETE FROM tv_trace WHERE userid=(%s) ;
                                    DELETE FROM tv_commit WHERE userid=(%s) ;
                                    DELETE FROM book_list WHERE userid=(%s) ;
                                    DELETE FROM book_trace WHERE userid=(%s) ;
                                    DELETE FROM comment_b WHERE userid=(%s) ;
                                    DELETE FROM users WHERE id=(%s) ;
                                         """
                    cursor.execute(statement,(idno,idno,idno,idno,idno,idno,idno,))
                    print("hhhhh")