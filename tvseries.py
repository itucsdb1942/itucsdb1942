import os
import sys
import psycopg2 as dbapi2
import dbinit as db

url=db.url

tv_data = [

     {'title': "Game of Thrones",
     'channel': "HBO",
     'language': "English",
     'season':7,
     'year':2011,
     'genre':"Fantastic"},

     {'title': "How I Met Your Mother",
     'channel': "Netflix",
     'language': "English",
     'season':9,
     'year':2004,
     'genre':"Sitcom"},

     {'title': "Undone",
     'channel': "Amazon",
     'language': "English",
     'season':1,
     'year':2019,
     'genre':"Science-Fiction"},

     {'title': "Black Mirror",
     'channel': "Netflix",
     'language': "English",
     'season':5,
     'year':2011,
     'genre':"Science-Fiction"},
]

tv_book = {}

with dbapi2.connect(url) as connection:
    with connection.cursor() as cursor:
            statement = """SELECT tvseries.title, channel.chan_name FROM tvseries, channel
                 WHERE(tvseries.channelid=channel.id); """
            cursor.execute(statement)
            for title, channel in cursor:
                tv_book['title']=title
                tv_book['channel']=channel
connection.close()

print(tv_book)

channel_ids = {}
try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
            for item in tv_data:
                channel_names = [item['channel']]
                
                for name in channel_names:
                    if name not in channel_ids:
                        statement = """INSERT INTO channel (chan_name) VALUES (%s)
                                    RETURNING id"""
                        cursor.execute(statement, (name,))
                        connection.commit()
                        channel_id = cursor.fetchone()[0]
                        channel_ids[name] = channel_id
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()

try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
                for item in tv_data:
                    statement = """INSERT INTO tvseries (TITLE, CHANNELID, LANGUAGE, YEAR, GENRE)
                                VALUES (%(title)s, %(channelid)s, %(language)s, %(year)s, %(genre)s)
                            RETURNING id;"""                
                
                    item['channelid'] = channel_ids[item['channel']]
                    
                    cursor.execute(statement,item)
                    connection.commit()
                    tv_id = cursor.fetchone()[0]
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()   
