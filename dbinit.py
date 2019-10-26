import os
import sys

import psycopg2 as dbapi2

 

INIT_STATEMENTS = [

    """
       """
]

#dsn = """user='postgres' password='docker'
 #       host='localhost' port=5432 dbname='mydatabase'"""


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
           cursor.execute(statement)
        cursor.close()


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
