import os
import sys
import psycopg2 as dbapi2
import dbinit as db

url=db.url
class Episode:
     def __init__(self, id,tv,name,season_n,episode_n):
        self.id=id
        self.tv=tv
        self.name=name
        self.season_n=season_n
        self.episode_n=episode_n

class TV:
    def __init__(self, id=None,title=None,language=None,year=None,season=None,genre=None,channel=None,vote=None,score= None):
        self.id=id
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

    def print_episode(self,se_number):
        ep_list=[]
        with dbapi2.connect(url) as connection:
            with connection.cursor() as cursor:
                    statement = """SELECT ID, name, number FROM episode
                                    WHERE tvid = (%s) AND season_n = (%s); """
                    cursor.execute(statement,(self.id,se_number,))
                    for id, name,ep_number in cursor:
                        episode = Episode(id,self.id,name,se_number,ep_number)
                        ep_list.append(episode)
        connection.close()
        return ep_list

    def addtv(self):
  
        try:
            with dbapi2.connect(url) as connection:
                with connection.cursor() as cursor:
                            statement = """INSERT INTO tvseries (TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE)
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                    RETURNING id;"""                
                            cursor.execute(statement,(self.title,self.channel,self.language,self.year,self.season,self.genre,))
                            connection.commit()
                            self.id = cursor.fetchone()[0]
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            connection.close()  

    


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
    {'season': 2,
     'episode': 1,
     'title': "The North Remembers"},
    {'season': 2,
     'episode': 2,
     'title': "The Night Lands"},
    {'season': 2,
     'episode': 3,
     'title': "What Is Dead May Never Die"},
    {'season': 2,
     'episode': 4,
     'title': "Garden of Bones"},
    {'season': 2,
     'episode': 5,
     'title': "The Ghost of Harrenhal"},
    {'season': 2,
     'episode': 6,
     'title': "The Old Gods and the New"},
    {'season': 2,
     'episode': 7,
     'title': "A Man Without Honor"},
    {'season': 2,
     'episode': 8,
     'title': "The Prince of Winterfell"},
      {'season': 2,
     'episode': 9,
     'title': "Black Water"},
    {'season': 2,
     'episode': 10,
     'title': "Valar Morghulis"},
     
]

try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
                for item in tv_data:
                    statement = """INSERT INTO tvseries (TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE)
                                VALUES (%(title)s, %(channel)s, %(language)s, %(year)s, %(season)s, %(genre)s)
                            RETURNING id;"""    
                    cursor.execute(statement,item)
                    connection.commit()
                    tv_id = cursor.fetchone()[0]
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()  

tv_book={}
with dbapi2.connect(url) as connection:
    with connection.cursor() as cursor:
            statement = """SELECT id, title FROM tvseries; """
            cursor.execute(statement)
            for id, name in cursor:
                tv_book[name]=id
connection.close()

try:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
                for item in got_data:
                    print("lol")
                    statement = """INSERT INTO episode (tvid, name, number, season_n)
                                VALUES (%(tvid)s, %(title)s, %(episode)s, %(season)s)
                            RETURNING id;"""                
                    item['tvid'] = tv_book['Game of Thrones']
                    cursor.execute(statement,item)
                    connection.commit()
                    episode_id = cursor.fetchone()[0]
except dbapi2.DatabaseError:
    connection.rollback()
finally:
    connection.close()   
  
def print_tv():
    tv_list=[]
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
                statement = """SELECT ID, TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE, VOTE, SCORE FROM tvseries; """
                cursor.execute(statement)
                for id, title, channel, lang, year, season, genre, vote, score in cursor:
                    tv =TV(id,title,lang,year,season,genre,channel,vote,score)
                    tv_list.append(tv)
    connection.close()
    return tv_list
    
def find_tv(idno):
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:
                statement = """SELECT ID, TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE, VOTE, SCORE FROM tvseries WHERE id=%s; """
                cursor.execute(statement,(idno,))
                for id, title, channel, lang, year, season, genre, vote, score in cursor:
                    tv =TV(id,title,lang,year,season,genre,channel,vote,score)
    connection.close()
    return tv