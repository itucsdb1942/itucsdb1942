import os
import sys

import psycopg2 as dbapi2

class tvdb():
    def __init__(self,idd="null",name="null",ep="null"):
        self.idd=idd
        self.name=name
        self.ep=ep

INIT_STATEMENTS = [
    """SELECT * FROM tvseries;
    """
   
]

#dsn = """user='postgres' password='docker'
 #       host='localhost' port=5432 dbname='mydatabase'"""
printf = tvdb()

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
            for row in cursor:
                idd, title, ep = row
                printf.name = title
                printf.idd = idd
                printf.ep = ep

                
        cursor.close()
        

def a():
    return printf

if __name__ == "__main__":
    print(44)
else:
    print("555")
    url = os.getenv("python dbinit.py", "postgres://yqplkmdw:6ZAgWY_E0tcKhin3yUXcgbtQ0RJ7Sf43@manny.db.elephantsql.com:5432/yqplkmdw")
    print(url)
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
