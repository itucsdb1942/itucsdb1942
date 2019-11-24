import os
import sys
import psycopg2 as dbapi2
import dbinit as db
from flask_login import UserMixin
url=db.url

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
            with dbapi2.connect(url) as connection:
                with connection.cursor() as cursor:
                            statement = """INSERT INTO users (name, surname, username, mail, gender, birth, password)
                                        VALUES (%(name)s, %(surname)s, %(username)s, %(mail)s, %(gender)s, %(birth)s, %(password)s)
                                    RETURNING id;"""       
                            cursor.execute(statement,user_data)
                            connection.commit()
                            user_id = cursor.fetchone()[0]
        except dbapi2.DatabaseError:
            connection.rollback() 
        finally:
            connection.close()   

    
def get(user_id):
        with dbapi2.connect(url) as connection:
            with connection.cursor() as cursor:
                    statement = """SELECT id, name, surname, username, mail, gender, birth, password FROM users 
                                        WHERE id = ({}); """.format(user_id)
                    cursor.execute(statement)
                    user= False
                    for i, n, s, u, m, g, b, p  in cursor:
                        user= User(id=i, name=n, surname=s, username=u,
                        mail=m, gender=g, date=b, password=p)
                    return user
        connection.close()

def username_check(username):
        with dbapi2.connect(url) as connection:
            with connection.cursor() as cursor:
                    statement = """SELECT id, name, surname, username, mail, gender, birth, password FROM users 
                                        WHERE username = (%s); """
                    cursor.execute(statement,(username,))
                    user= False
                    for i, n, s, u, m, g, b, p  in cursor:
                        user= User(id=i, name=n, surname=s, username=u,
                        mail=m, gender=g, date=b, password=p)
                    return user
        connection.close()
    
def mail_check(mail):
        with dbapi2.connect(url) as connection:
            with connection.cursor() as cursor:
                    statement = """SELECT id, name, surname, username, mail, gender, birth, password FROM users 
                                        WHERE mail = (%s); """
                    cursor.execute(statement,(mail,))
                    user= False
                    for i, n, s, u, m, g, b, p  in cursor:
                        user= User(id=i, name=n, surname=s, username=u,
                        mail=m, gender=g, date=b, password=p)
                    return user
        connection.close()


