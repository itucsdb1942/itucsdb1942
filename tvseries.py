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
]

tv_book = {}

with dbapi2.connect(url) as connection:
    with connection.cursor() as cursor:
            statement = """SELECT tvseries.title, channel.chan_name FROM tvseries, channel
                 WHERE(tvseries.channelid=channel.id); """
            cursor.execute(statement)
            for title, channel in cursor:
                print('{}: {}'.format(title, channel))
                tv_book['title']=title
                tv_book['channel']=channel
connection.close()

print(tv_book)

if (tv_data['title']!=tv_book['title'] and tv_data['channel']!=tv_book['channel']):
    channel_ids = {}
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
            for item in tv_data:
                channel_names = [item['channel']]
                print(11)
                for name in channel_names:
                    if name not in channel_ids:
                        statement = """INSERT INTO channel (chan_name) VALUES (%s)
                                    RETURNING id"""
                        cursor.execute(statement, (name,))
                        connection.commit()
                        channel_id = cursor.fetchone()[0]
                        channel_ids[name] = channel_id
    connection.close()

    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
            for item in tv_data:
                statement = """INSERT INTO tvseries (TITLE, CHANNELID, LANGUAGE, YEAR, GENRE)
                            VALUES (%(title)s, %(channel_id)s, %(language)s, %(year)s, %(genre)s)
                    RETURNING id;"""
                
                item['channel_id'] = channel_ids[item['channel']]
                cursor.execute(statement,item)
                connection.commit()
                book_id = cursor.fetchone()[0]
    

    connection.close()