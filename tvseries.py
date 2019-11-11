import os
import sys
import psycopg2 as dbapi2
import dbinit as db

url=db.url

tv_data = [

     {'title': "Game of Thrones",
     'channel': "HBO",
     'language': "English",
     'season':8,
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

got_data=[

    {'season': 1,
     'episode': 1,
     'title': "Winter Is Coming"},
    {'season': 1,
     'episode': 2,
     'title': "The Kingsroad"},
    {'season': 1,
     'episode': 3,
     'title': "Lord Snow"},
    {'season': 1,
     'episode': 4,
     'title': "Cripples, Bastards, and Broken Things"},
    {'season': 1,
     'episode': 5,
     'title': "The Wolf and the Lion"},
    {'season': 1,
     'episode': 6,
     'title': "A Golden Crown"},
    {'season': 1,
     'episode': 7,
     'title': "You Win or You Die"},
    {'season': 1,
     'episode': 8,
     'title': "The Pointy End"},
      {'season': 1,
     'episode': 9,
     'title': "Baelor"},
    {'season': 1,
     'episode': 10,
     'title': "Fire and Blood"},
]

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

channel_book={}
with dbapi2.connect(url) as connection:
    with connection.cursor() as cursor:
            statement = """SELECT channel.id, channel.chan_name FROM channel; """
            cursor.execute(statement)
            for id, name in cursor:
                channel_book[name]=id
connection.close()

try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
                for item in tv_data:
                    statement = """INSERT INTO tvseries (TITLE, CHANNELID, LANGUAGE, YEAR, SEASON, GENRE)
                                VALUES (%(title)s, %(channelid)s, %(language)s, %(year)s, %(season)s, %(genre)s)
                            RETURNING id;"""                
                
                    item['channelid'] = channel_book[item['channel']]
                    
                    cursor.execute(statement,item)
                    connection.commit()
                    tv_id = cursor.fetchone()[0]
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()   



class TV:
    def __init__(self, title,language,year,season,genre,channel,vote,score):
        self.title=title
        self.language=language
        self.year=year
        self.season=season
        self.genre=genre
        self.channel=channel
        self.vote=vote
        self.score=score

    def print(self):
        print(self.title,self.channel,self.year,self.genre,self.season,self.language,self.vote,self.score)

def print_tv():
    tv_list=[]
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
                statement = """SELECT TITLE, CHANNELID, LANGUAGE, YEAR, SEASON, GENRE, VOTE, SCORE FROM tvseries; """
                cursor.execute(statement)
                for title, channelid, lang, year, season, genre, vote, score in cursor:
                    with dbapi2.connect(url) as connection2:
                         with connection.cursor() as cursor2:
                            statement = """SELECT channel.chan_name FROM channel
                                            WHERE channel.id = %s ; """
                            cursor2.execute(statement,(channelid,))
                            channel = cursor2.fetchone()[0]
                    connection2.close()
                    tv =TV(title,lang,year,season,genre,channel,vote,score)
                    tv_list.append(tv)
    connection.close()
    return tv_list
    
