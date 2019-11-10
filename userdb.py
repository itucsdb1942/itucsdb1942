import os
import sys
import psycopg2 as dbapi2
import dbinit as db

url=db.url

class User():
    def __init__(self, name,surname,username,mail,gender,date,password):
        self.name=name
        self.surname=surname
        self.username=username
        self.mail=mail
        self.gender=gender
        self.date=date
        self.password=password
    def display(self):
    
      print(self.name,
        self.surname,
        self.username,
        self.mail,
        self.gender,
        self.date,
        self.password)

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




