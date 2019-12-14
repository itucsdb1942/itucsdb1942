import os
import sys
import psycopg2 as dbapi2
import dbinit as db
from datetime import datetime

connection=db.connection
cursor=connection.cursor()

class commit:
    def __init__(self,id=0,username=0,tvid=0,header=0,content=0,date=0,like=0,dislike=0):
        self.id=id
        self.username=username
        self.tvid=tvid
        self.header=header
        self.content=content
        self.like=like
        self.date=date
        self.dislike=dislike
    
   

    def com_like_number(self,userid):
            statement = """ SELECT LIKE_N FROM tv_commit
                        WHERE userid = %s AND id = %s;"""
            cursor.execute(statement, ( userid, self.id,))
            like_n=cursor.fetchone()[0]
            connection.commit()
            return like_n

    def com_dislike_number(self,userid):
            statement = """ SELECT DISLIKE_N FROM tv_commit
                        WHERE userid = %s AND id = %s;"""
            cursor.execute(statement, ( userid, self.id,))
            dislike_n=cursor.fetchone()[0]
            connection.commit()
            return dislike_n

def com_like(commitid):
            statement = """ UPDATE tv_commit
                        SET like_n = like_n+1 WHERE id = %s;"""
            cursor.execute(statement, ( commitid,))
            connection.commit()
        

def com_dislike(commitid):
            statement = """ UPDATE tv_commit
                        SET dislike_n = dislike_n + 1 WHERE id = %s;"""
            cursor.execute(statement, (  commitid,))
            connection.commit()

class Episode:
    def __init__(self, id,tv,name,season_n,episode_n):
        self.id=id
        self.tv=tv
        self.name=name
        self.season_n=season_n
        self.episode_n=episode_n

    def checkEpisodeWatched(self,userid,season):
                        check=0
                        statement = """SELECT watched FROM tv_trace
                                        WHERE episodeid = (%s) AND userid = (%s); """
                        cursor.execute(statement,(self.id,userid,))
                        for watched in cursor:
                            if watched[0]==True:
                                check=check+1
                        connection.commit()

                        if check>0:
                            return True
                        else:
                            return False
                    


def episodewatched(userid,episodeid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO tv_trace (userid, episodeid, watched)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,episodeid,"TRUE"))
                connection.commit()
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            with connection.cursor() as cursor:
                statement = """ DELETE FROM tv_trace 
                            WHERE userid = %s AND episodeid = %s"""
                cursor.execute(statement, ( userid, episodeid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            connection.rollback()
            cursor=connection.cursor()
        

def seasonwatched(userid,tvid,season):
            episodeids=[]
            with connection.cursor() as cursor:
                statement = """SELECT ID FROM episode
                                WHERE tvid = (%s) AND season_n = (%s); """
                cursor.execute(statement,(tvid,season,))
                for id in cursor:
                    episodeids.append(id)
                connection.commit()
    
            try:
                    with connection.cursor() as cursor:
                        for item in episodeids:
                            statement = """INSERT INTO tv_trace (userid, episodeid, watched)
                                                VALUES ( (%s), (%s), (%s))
                                            RETURNING id;"""
                            cursor.execute(statement,(userid,item,"TRUE"))
                            connection.commit()

            except dbapi2.errors.UniqueViolation:
                        connection.rollback()
                        with connection.cursor() as cursor:
                            for item in episodeids:
                                statement = """ DELETE from tv_trace 
                                                    WHERE userid = (%s) AND episodeid =(%s);"""
                                cursor.execute(statement, ( userid, item,))
                                connection.commit()
               
        
        
    



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
                        statement = """SELECT ID, name, number FROM episode
                                        WHERE tvid = (%s) AND season_n = (%s); """
                        cursor.execute(statement,(self.id,se_number,))
                        for id, name,ep_number in cursor:
                            episode = Episode(id,self.id,name,se_number,ep_number)
                            ep_list.append(episode)
            
                        return ep_list

        def addtv(self):
    
            try:
                with connection.cursor() as cursor:
                                statement = """INSERT INTO tvseries (TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE)
                                            VALUES (%s, %s, %s, %s, %s, %s)
                                        RETURNING id;"""                
                                cursor.execute(statement,(self.title,self.channel,self.language,self.year,self.season,self.genre,))
                                connection.commit()
                                self.id = cursor.fetchone()[0]
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
                  

        def tv_percent(self,userid):
                        checkall=0
                        checkw=0
                        episodeid=[]
                        statement="""SELECT episode.id FROM episode WHERE episode.tvid = (%s)"""
                        cursor.execute(statement,(self.id,))
                        for item in cursor:
                            checkall=checkall+1
                            episodeid.append(item)
                        if checkall==0:
                            return 0
                        for a in episodeid:
                            statement = """SELECT tv_trace.id FROM tv_trace
                                            WHERE tv_trace.episodeid = (%s) AND userid = (%s); """
                            cursor.execute(statement,(a,userid,))
                            for watched in cursor:
                                checkw=checkw+1
                                
                        connection.commit()
                        percent=checkw*100/checkall
                        if(percent==100.0):
                            watched_add(userid,self.id)
                        if(percent>0.0):
                            watching_add(userid,self.id)
                        return checkw*100/checkall

        def season_percent(self,userid,season_n):
                        checkall=0
                        checkw=0
                        episodeid=[]

                        statement = """SELECT episode.id FROM tvseries,episode
                                        WHERE episode.tvid = (%s) AND episode.season_n=(%s); """
                        cursor.execute(statement,(self.id,season_n,))
                        for all in cursor:
                            checkall=checkall+1
                            episodeid.append(all)
                        if (checkall==0):
                            return 0
                        for a in episodeid:
                            statement = """SELECT tv_trace.id FROM tv_trace
                                            WHERE tv_trace.episodeid = (%s) AND userid = (%s); """
                            cursor.execute(statement,(a,userid,))
                            for watched in cursor:
                                checkw=checkw+1
                        connection.commit()
                
                        return checkw*100/checkall

        def check_fav(self,userid):
                connection.rollback()
                try:
                    with connection.cursor() as cursor:
                        statement = """ SELECT fav_list FROM tv_list
                                    WHERE userid = %s AND tvid = %s;"""
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
                        statement = """ SELECT hate_list FROM tv_list
                                    WHERE userid = %s AND tvid = %s;"""
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
                        statement = """ SELECT wish_list FROM tv_list
                                    WHERE userid = %s AND tvid = %s;"""
                        cursor.execute(statement, ( userid, self.id,))
                        connection.commit()
                        check=cursor.fetchone()[0]
                        if check==False:
                            return False
                        return True
                except:
                    return False
        
def submit_commit(tvid,userid,header,context):
            now = datetime.now()
            try:
                with connection.cursor() as cursor:
                                statement = """INSERT INTO tv_commit (userid, tvid, header, content,date)
                                            VALUES (%s, %s, %s, %s, %s)
                                        RETURNING id;"""                
                                cursor.execute(statement,(userid,tvid,header,context,now))
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
                  

def print_commit(tvid,userid):
            commits=[]
            try:
                with connection.cursor() as cursor:
                                statement = """SELECT username FROM users
                                             WHERE id=(%s);"""                
                                cursor.execute(statement,(userid,))
                                username=cursor.fetchone()[0]
                                statement = """SELECT id,header,content,date FROM tv_commit
                                             WHERE userid=(%s) AND tvid=(%s) ORDER BY date DESC;"""                
                                cursor.execute(statement,(userid,tvid))
                                for id,head,cont,date in cursor:
                                    com=commit(id=id, username=username,tvid=tvid,header=head,content=cont,date=date)
                                    commits.append(com)  
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
                  
            return commits
def print_watching():
    tvs={}
    try:
        with connection.cursor() as cursor:
                                statement = """SELECT tvid FROM tv_list
                                             WHERE watching_list=TRUE;"""                
                                cursor.execute(statement,)
                                for tvid in cursor:
                                    print("hhhh")
                                    statement = """SELECT title FROM tvseries
                                                WHERE id=(%s);"""                
                                    cursor.execute(statement,(tvid))
                                    for tvname in cursor:
                                        tvs[tvid]=tvname
                                    connection.commit()
                                return tvs
    except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
                  

def fav_add(userid, tvid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO tv_list (userid, tvid, fav_list)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,tvid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            
            a="FALSE"
            with connection.cursor() as cursor:    
                statement = """ SELECT fav_list FROM tv_list
                            WHERE userid = %s AND tvid = %s;"""
                cursor.execute(statement, ( userid, tvid,))
                print("except")
                check=cursor.fetchone()[0]
                print("ddd")
                if check == False:
                    a="TRUE"
                statement = """ UPDATE tv_list 
                            SET fav_list = %s WHERE userid = %s AND tvid = %s"""
                cursor.execute(statement, (a, userid, tvid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            print("hata")
            connection.rollback()
            cursor=connection.cursor()     

def hate_add(userid, tvid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO tv_list (userid, tvid, hate_list)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,tvid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            
            a="FALSE"
            with connection.cursor() as cursor:    
                statement = """ SELECT hate_list FROM tv_list
                            WHERE userid = %s AND tvid = %s;"""
                cursor.execute(statement, ( userid, tvid,))
                print("except")
                check=cursor.fetchone()[0]
                print("ddd")
                if check == False:
                    a="TRUE"
                statement = """ UPDATE tv_list 
                            SET hate_list = %s WHERE userid = %s AND tvid = %s"""
                cursor.execute(statement, (a, userid, tvid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            print("hata")
            connection.rollback()
            cursor=connection.cursor()    

def wish_add(userid, tvid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO tv_list (userid, tvid, wish_list)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,tvid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            
            a="FALSE"
            with connection.cursor() as cursor:    
                statement = """ SELECT wish_list FROM tv_list
                            WHERE userid = %s AND tvid = %s;"""
                cursor.execute(statement, ( userid, tvid,))
                print("except")
                check=cursor.fetchone()[0]
                print("ddd")
                if check == False:
                    a="TRUE"
                statement = """ UPDATE tv_list 
                            SET wish_list = %s WHERE userid = %s AND tvid = %s"""
                cursor.execute(statement, (a, userid, tvid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            print("hata")
            connection.rollback()
            cursor=connection.cursor()  

def watched_add(userid, tvid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO tv_list (userid, tvid, watched_list)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,tvid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            
            with connection.cursor() as cursor:    
              
                statement = """ UPDATE tv_list 
                            SET watched_list = %s,  watching_list = %s WHERE userid = %s AND tvid = %s"""
                cursor.execute(statement, ("TRUE","FALSE", userid, tvid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            print("hata")
            connection.rollback()
            cursor=connection.cursor()          

def watching_add(userid, tvid):
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO tv_list (userid, tvid, watching_list)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,tvid,"TRUE"))
                connection.commit()
                
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            
            with connection.cursor() as cursor:    
                statement = """ UPDATE tv_list 
                            SET watched_list = %s,  watching_list = %s WHERE userid = %s AND tvid = %s"""
                cursor.execute(statement, ("FALSE","TRUE", userid, tvid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            print("hata")
            connection.rollback()
            cursor=connection.cursor()  
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
    cursor=connection.cursor()

      

tv_book={}
with connection.cursor() as cursor:
            statement = """SELECT id, title FROM tvseries; """
            cursor.execute(statement)
            for id, name in cursor:
                tv_book[name]=id


try:
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
    cursor=connection.cursor()

       
  
def print_tv():
                tv_list=[]
    
                statement = """SELECT ID, TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE, VOTE, SCORE FROM tvseries; """
                cursor.execute(statement)
                for id, title, channel, lang, year, season, genre, vote, score in cursor:
                    tv =TV(id,title,lang,year,season,genre,channel,vote,score)
                    tv_list.append(tv)
    
                return tv_list
    
def find_tv(idno):
                statement = """SELECT ID, TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE, VOTE, SCORE FROM tvseries WHERE id=%s; """
                cursor.execute(statement,(idno,))
                for id, title, channel, lang, year, season, genre, vote, score in cursor:
                    tv =TV(id,title,lang,year,season,genre,channel,vote,score)
                return tv