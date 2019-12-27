Parts Implemented by Member Name
================================

1. Database Structure
=====================

In general, I took part in the operations of users and TVSeries tracking. As an extra I have provided login management to the app.

2. Sign Up Page
===============

For users, a class named User was first created in the userdb.py file.

   .. code-block:: python

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

By creating a method named adduser to this class, users row insert operation to database is performed.
 
   .. code-block:: python

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

Additional username_check and mail_check functions are written to the userdb.py file to check whether the data sent is in the database.

   .. code-block:: python

      def username_check(username):
            with connection.cursor() as cursor:
                    statement = """SELECT id, name, surname, username, mail, gender, birth, password FROM users 
                                        WHERE username = (%s); """
                    cursor.execute(statement,(username,))
                    user= False
                    for i, n, s, u, m, g, b, p  in cursor:
                        user= User(id=i, name=n, surname=s, username=u,
                        mail=m, gender=g, date=b, password=p)
                    return user


Flask_wtf was used to get inputs easily. To do this, a forms.py file was created and a class named registrationForm was created. Here, the validations of the information required for the user to register are determined and extra validates are written for the pre-existing username and e-mail. The username_check and mail_check functions in the userdb.py file were used for these validates.

   .. code-block:: python

      class registirationForm(FlaskForm):
            name=StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
            surname=StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
            username=StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
            mail =StringField('Mail', validators=[DataRequired(), Email()])
            gender=RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
            date=DateField('Date of Birth', validators=[DataRequired()])
            password = PasswordField('Password', validators=[DataRequired()])
            confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
            submit = SubmitField('Sign Up')

            def validate_username(self, username):
                user = username_check(username.data)
                if user: 
                    raise ValidationError('That username is taken!')

            def validate_mail(self, mail):
                user = mail_check(mail.data)
                if user: 
                    raise ValidationError('That e-mail is taken!')

Sign up page was created using flask in server.py file. Here the registrationForm class in the forms.py file was called and used in the site. By using Flask_bcrypt, we have encrypted the user's password and securely added it to the database. If the sign-up was successfully completed, the log-in page was redirected and the success alert was printed. If any error occurs, error alert is displayed.

   .. code-block:: python

      @app.route("/signup", methods=['GET', 'POST'])

        def signup_page():
            form=registirationForm()
            if request.method =='POST':
                if form.validate_on_submit():
                    crypt_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8') #creating hashed password
                    flash(f'Account Created for {form.username.data}! Now You Can Login.', 'success')
                    user=User(name=form.name.data, surname=form.surname.data, username=form.username.data,
                                mail=form.mail.data, gender=form.gender.data, date=form.date.data, password=crypt_password)
                    user.adduser()
                    return redirect(url_for('login_page'))
                else:
                    flash(f'Failed to Create Account for {form.username.data}!', 'danger')

            return render_template("signup.html", form=form)

In the design of the site, when there is a validation, it is provided to press error under the input places.

   .. code-block:: HTML

      {% if form.name.errors %} {{form.name(type="text" , class="form-control is-invalid" , placeholder="Name")}}
                                <div class="invalid-feedback">
                                    {% for error in form.name.errors %}
                                    <span>{{ error }}</span> {% endfor %}
                                </div>
                                {% else %} {{form.name(type="text" , class="form-control" , placeholder="Name" )}}{% endif%}

3. Login Management
===================

The flask_login library was used for Login Management.

        .. code-block:: python

            from flask_login import LoginManager,login_user, current_user, logout_user, login_required 


The user_loader function of the login manager was implemented by making a get function in the userdb.py file.

   .. code-block:: python

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

   .. code-block:: python

      @login_manager.user_loader
      def load_user(user_id):
            return get(int(user_id))


@Login_required has been added under the app.route of the pages that should not be accessed without login.

       .. code-block:: python

          @app.route("/home", methods=['GET', 'POST'])
          @login_required
          ..


Logout operation implemented.

       .. code-block:: python

          @app.route("/logout")
          def logout():
                logout_user()
                return redirect(url_for('login_page'))

    
4. Home Page
============

For the home page, functions were first written in the tvseries.py file and in the books.py file to print the lists. (The books.py file is made by my groupmate.) 


The functions in TVseries are print_watching, print_watched, print_wish, print_fav, print_hate. The sample code is given below.
    
    .. code-block:: python

          def print_wish(idno):
                tvs={}
                try:
                    with connection.cursor() as cursor:
                                            statement = """SELECT tv_list.tvid, tvseries.title FROM tv_list,tvseries
                                                        WHERE tv_list.wish_list=TRUE AND tvseries.id=tv_list.tvid AND userid=%s;"""                
                                            cursor.execute(statement,(idno,))
                                            for tvid, tvname in cursor:
                                                tvs[tvid]=tvname
                                            connection.commit()
                                            return tvs
                except dbapi2.DatabaseError:
                            connection.rollback()
                            cursor=connection.cursor() 

These lists were sent to the site and printed.
        
For site design, a for loop was created to show the lists. Also when clicking on tvseries or book, it was made to go to their page.


        .. code-block:: HTML

           <h2 class="heading-section mb-4">Watching List</h2>
                {% if watching != None %} {% for item in watching %}

                <h2 class="heading-section mb-3">
                    <a class="text-white-50" href="/tv/{{item}}">
                        <i span style="color:yellow" class="ion-ios-film mr-2"></i> {{watching[item]}}
                        <br></a>
                </h2>
                {% endfor %}{% endif %}

5. TV Series Page
=================

The tvseries.py file was first created for the database operations of the tv series page. In this file, a class named TV has been created.

 .. code-block:: python

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

                
Then a function named print_tv () was written to see all tvseries in the database.


 .. code-block:: python

        def print_tv():
                        tv_list=[]
            
                        statement = """SELECT ID, TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE, VOTE, SCORE FROM tvseries ORDER BY id; """
                        cursor.execute(statement)
                        for id, title, channel, lang, year, season, genre, vote, score in cursor:
                            tv =TV(id,title,lang,year,season,genre,channel,vote,score)
                            tv_list.append(tv)
            
                        return tv_list

Print_tv_by_az (), print_tv_by_score (), print_tv_by_year () functions were written for sort operations.

 .. code-block:: python
        def print_tv_by_az():
                tv_list=[]
    
                statement = """SELECT ID, TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE, VOTE, SCORE FROM tvseries ORDER BY title; """
                cursor.execute(statement)
                for id, title, channel, lang, year, season, genre, vote, score in cursor:
                    tv =TV(id,title,lang,year,season,genre,channel,vote,score)
                    tv_list.append(tv)
    
                return tv_list

TV_percent method of TV class was created for the tvseries tracking progress. 

Here, according to the percentage of progress, watched and watching list columns in the tv_list table inserted or updated with watched_add, watching_add, notwatch_add
functions in tvseries.py. (These functions will be explained later.)

 .. code-block:: python

        def tv_percent(self,userid):
                        checkall=0
                        checkw=0
                        statement="""SELECT COUNT(episode.id) FROM episode WHERE episode.tvid = (%s)"""
                        cursor.execute(statement,(self.id,))
                        checkall=cursor.fetchone()[0]
                        
                        if checkall==0:
                            return 0
                        statement = """SELECT COUNT(tv_trace.id) FROM tv_trace,episode,tvseries
                                            WHERE tvseries.id=%s AND tvseries.id= episode.tvid AND tv_trace.episodeid = episode.id AND userid = (%s); """
                        cursor.execute(statement,(self.id,userid,))
                        checkw=cursor.fetchone()[0]
                        connection.commit()
                        percent=checkw*100/checkall
                        if(percent==100.0):
                            watched_add(userid,self.id)
                        elif(percent>0.0):
                            watching_add(userid,self.id)
                        elif(percent==0.0):
                            notwatch_add(userid,self.id)
                        return checkw*100/checkall


A function named season_percent has been created for the progress of the specific season.

 .. code-block:: python

        def season_percent(self,userid,season_n):
                        checkall=0
                        checkw=0

                        statement = """SELECT COUNT(episode.id) FROM episode
                                        WHERE episode.tvid = (%s) AND episode.season_n=(%s); """
                        cursor.execute(statement,(self.id,season_n,))
                        checkall=cursor.fetchone()[0]
                        if (checkall==0):
                            return 0
                        statement = """SELECT COUNT(tv_trace.id) FROM tv_trace,episode,tvseries
                                            WHERE tvseries.id=%s AND tvseries.id= episode.tvid AND tv_trace.episodeid = episode.id AND userid = (%s) AND episode.season_n=(%s); """
                        cursor.execute(statement,(self.id,userid,season_n))
                        checkw=cursor.fetchone()[0]
                        connection.commit()
                
                        return checkw*100/checkall

The seasonwatched function was written for the season watch button. Here, if the user has watched that season, the try except method was used to delete those lines.

 .. code-block:: python

        def seasonwatched(userid,tvid,season):
            connection.rollback()
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

The tvpage web page was created in the server.py file, and it was determined which sort order according to its extension. When clicking on tvseries, the post method was used to redirect to its web page. Another post method was created for the season watch button.

 .. code-block:: python

        @app.route("/tv/<string:sort>", methods=['GET', 'POST'])
        @login_required

        def tvpage(sort):
            if sort=="sortbyaz":
                tvs=print_tv_by_az()
            elif sort=="sortbyscore":
                tvs=print_tv_by_score()
            elif sort=="sortbyyear":
                tvs=print_tv_by_year()
            elif sort=="sortbydefault":
                tvs=print_tv()
            
            if request.method =='POST':
                try:
                    item=request.form['form_id']
                    return redirect(url_for('tv',item=item))
                except:
                    pass
                try:
                    tvid=request.form['tvid']
                    season=request.form['sezon']
                    seasonwatched(current_user.id,tvid,season)
                except:
                    pass
                
            return render_template("tvpage.html", tv=tvs)




In tvpage.html, a dropdown was created for sort operations.

 .. code-block:: HTML

        <div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
                            <a class="dropdown-item" name="arrange" value="sortbyaz" href="/tv/sortbyaz">Sort by A-Z</a>
                            <a class="dropdown-item" name="arrange" value="sortbyscore" href="/tv/sortbyscore">Sort by Score</a>
                            <a class="dropdown-item" name="arrange" value="sortbyyear" href="/tv/sortbyyear">Sort by Year</a>
                        </div>


A hidden form was created to go to the dynamic page of any tvseries. Also, the tv_percent function has colored the icon of the tvseries according to the viewing status.

 .. code-block:: HTML

        {% for item in tv %}
            <div class="col-lg-6 mb-5 mb-md-0">
                <form id="tv-form{{item.id}}" action="" method="POST">
                    <input type="hidden" name="form_id" value="{{item.id}}" />
                    <h2 class="heading-section mb-3"> <a class="text-white-50" href="javascript:{}" onclick="document.getElementById('tv-form{{item.id}}').submit();">
                        {% if item.tv_percent(current_user.id) == 100.0 %}
                        <i span style="color:green" class="ion-ios-film mr-2"></i>
                        {% elif item.tv_percent(current_user.id)== 0.0 %}
                        <i span style="color:red"  class="ion-ios-film mr-2"></i>
                        {% else %}<i span style="color:yellow"  class="ion-ios-film mr-2"></i>
                        {% endif %}
                        {{item.title}}
                        <br></a></h2>

                </form>



For the seasons, the loop was created and the buttons were functionalized with the form. With the season_percent function, the watch button was colored and a progress bar was made.
 
 .. code-block:: HTML

        {% for season in range(1, item.season+1) %}
        {% with progress = item.season_percent(current_user.id,season) %}
            <div>Season {{season}}
                    <form id="tvid{{item.id}}" action="" method="POST">
                    {% if progress== 100.0 %}
                     <button name="watched" id="button{{item.id}}.{{season}}" class="btn btn-icon btn-primary btn-link" onclick="change('button{{item.id}}.{{season}}')"><i class="ion-ios-eye"></i></button> 
                     {% else %}   
                     <button name="watched" id="button{{item.id}}.{{season}}" class="btn btn-icon btn-dark btn-link" onclick="change('button{{item.id}}.{{season}}')"><i class="ion-ios-eye"></i></button>
                      {% endif %}
                            <input type="hidden" name="tvid" value="{{item.id}}"
                            <input type="hidden" name="sezon" value"{{season}}" />
                    </form>

                    <div class="progress mb-2" style="height: 15px;">

                        <div class="progress-bar progress-bar-striped" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: {{progress}}%;">
                                <span>{{progress}}% Complete</span>
                        </div>
        {% endwith %}
            </div>
            </div>
        {% endfor %}

6. Add TV Series Page
=====================

This page is accessed via the button at the beginning of the tvpage.


A form class named tvForm was created in forms.py for adding tvseries to the database.

 .. code-block:: python

        class tvForm(FlaskForm):
            title= StringField('Title',validators=[DataRequired()])
            language= StringField('Language',validators=[DataRequired()])
            year= IntegerField('Year',validators=[DataRequired()])
            season= IntegerField('Season',validators=[DataRequired()])
            genre= StringField('Genre',validators=[DataRequired()])
            channel= StringField('Channel',validators=[DataRequired()])
            submit = SubmitField('Add Tv Series')


The addtv function has been added to the TV class in the tvseries.py file.

 .. code-block:: python

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

In server.py, the addtv page was created with the same logic as the sign up page. A redirect is provided to the home page if the operation is successful.

 .. code-block:: python

        @app.route("/addtv", methods=['GET', 'POST'])
        @login_required
        def tvform_page():
            form=tvForm()
            if request.method =='POST':
                if form.validate_on_submit():
                    tv = TV(title=form.title.data,language=form.language.data, year=form.year.data,season=form.season.data,genre=form.genre.data,channel=form.channel.data)
                    tv.addtv()
                    flash(f'{form.title.data} is created!', 'success')
                    return redirect(url_for('home'))
            return render_template("addtv.html", form = form)


7. Dynamic Page of Tv Series
============================

First, the function named find_tv was written to tvseries.py to get the information of the tvseries with its id number.

 .. code-block:: python

        def find_tv(idno):
                statement = """SELECT ID, TITLE, CHANNEL, LANGUAGE, YEAR, SEASON, GENRE, VOTE, SCORE FROM tvseries WHERE id=%s; """
                cursor.execute(statement,(idno,))
                for id, title, channel, lang, year, season, genre, vote, score in cursor:
                    tv =TV(id,title,lang,year,season,genre,channel,vote,score)
                return tv

I will explain the content of these dynamic pages that host many processes by categorizing them.


7.1. TV Series List Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tv_list is a boolean table that checks if a tvseries belongs to which list. In this table, which has a total of 5 lists (columns), the control operation is for one tvseries in one line. Therefore, update operation was applied instead of delete operation.


To add tvseries to the list, the functions fav_add, hate_add and wish_add were written to tv_series.py.

 .. code-block:: python

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
                check=cursor.fetchone()[0]
                if check == False:
                    a="TRUE"
                statement = """ UPDATE tv_list 
                            SET fav_list = %s WHERE userid = %s AND tvid = %s"""
                cursor.execute(statement, (a, userid, tvid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            connection.rollback()
            cursor=connection.cursor() 

In addition, watched_add, watching_add, notwatch_add functions were written. Since they are related to each other, the update operations are performed accordingly.

 .. code-block:: python

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
                            SET watched_list = %s,  watching_list = %s WHERE userid = %s AND tvid = %s;"""
                cursor.execute(statement, ("TRUE","FALSE", userid, tvid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            connection.rollback()
            cursor=connection.cursor()          


Also check_fav, check_hate and check_wish functions were written to check if they are in the list. So if the TVseries is in that list the button is colored accordingly.

 .. code-block:: python

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

7.2. TV Series Episode Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, a class named Episode was created in the tvseries.py file.

 .. code-block:: python

    class Episode:
        def __init__(self, id,tv,name,season_n,episode_n):
            self.id=id
            self.tv=tv
            self.name=name
            self.season_n=season_n
            self.episode_n=episode_n

In order to print the episodes of a season, the method called print_episode was written to the TV class.

 .. code-block:: python

    class TV:
        ..
        def print_episode(self,se_number):
                        ep_list=[]
                        statement = """SELECT ID, name, number FROM episode
                                        WHERE tvid = (%s) AND season_n = (%s) ORDER BY number; """
                        cursor.execute(statement,(self.id,se_number,))
                        for id, name,ep_number in cursor:
                            episode = Episode(id,self.id,name,se_number,ep_number)
                            ep_list.append(episode)
            
                        return ep_list

The checkEpisodewatched method was written to check if the episode was watched.

 .. code-block:: python

    def checkEpisodeWatched(self,userid,season):
                        check=0
                        statement = """SELECT COUNT(id) FROM tv_trace
                                        WHERE episodeid = (%s) AND userid = (%s); """
                        cursor.execute(statement,(self.id,userid,))
                        check=cursor.fetchone()[0]
                        connection.commit()
                        if check>0:
                            return True
                        else:
                            return False

The episodewatched function is written to save the episode to the database. If the episode is already watched, the code is entered in except and the episode is removed from the tv_trace table.
 
 .. code-block:: python

    def episodewatched(userid,episodeid):
        connection.rollback()
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
        

7.2. TV Series Comment Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For comments, a class named commit was created in tvseries.py.

 .. code-block:: python

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

A function named print_commit was written to see all comments in the database.

 .. code-block:: python

    def print_commit(tvid):
            commits=[]
            try:
                with connection.cursor() as cursor:
                                statement = """SELECT tv_commit.id, tv_commit.header,tv_commit.content,tv_commit.date, users.username FROM tv_commit,users
                                             WHERE tv_commit.tvid=(%s) AND tv_commit.userid=users.id ORDER BY date DESC;"""                
                                cursor.execute(statement,(tvid,))
                                for id,head,cont,date,username in cursor:
                                    com=commit(id=id, username=username,tvid=tvid,header=head,content=cont,date=date)
                                    commits.append(com)  
                                
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
                  
            return commits

Com_like_number and com_dislike_number methods have been written to commit class to see how many dislike and dislike it takes.

 .. code-block:: python

    def com_like_number(self):
            statement = """ SELECT LIKE_N FROM tv_commit
                        WHERE  id = %s;"""
            cursor.execute(statement, (  self.id,))
            like_n=cursor.fetchone()[0]
            connection.commit()
            return like_n

The com_like and com_dislike update functions have been written to give comments like and dislike.

 .. code-block:: python

    def com_like(commitid):
            statement = """ UPDATE tv_commit
                        SET like_n = like_n+1 WHERE id = %s;"""
            cursor.execute(statement, ( commitid,))
            connection.commit()

Submit_commit function was added to add a new comment.

 .. code-block:: python

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

The delete_commit function was written to delete the comment. The delete button is only displayed in the current user's comments.

 .. code-block:: python

    def  delete_commit(idno, userid):
        try:
            with connection.cursor() as cursor:
                        statement = """ DELETE FROM tv_commit 
                                    WHERE userid = %s AND id = %s"""
                        cursor.execute(statement, ( userid, idno,))
                        connection.commit()
        except:
            connection.rollback()
            cursor=connection.cursor()

 .. code-block:: HTML

    {% for com in commit %}
    ..
    {% if current_user.username == com.username %}
                        <li class="nav-item mb-2">
                            <form action="" method="POST">
                                <div class="nav-link py-2">
                                    <button name="delete" value='{{com.id}}' class="btn btn-icon btn-primary btn-link"><i class="ion-ios-trash"></i></button>

                                </div>
                            </form>
                        </li>
    {% endif %}

7.2. TV Series Vote Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The add_scoret function was written to tvseries.py to update the score.

 .. code-block:: python

     def add_scoret(tvid,score):
        with connection.cursor() as cursor:
            statement = """ UPDATE tvseries
                                    SET SCORE = (SCORE*VOTE+%s)/(VOTE+1),VOTE=VOTE+1 WHERE id = %s;"""
            cursor.execute(statement, (score, tvid,))
            connection.commit()   
        cursor.close()

7.2. TV Series Delete Operation (For Admin User)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A function named delete_tv has been created in tvseries.py for this option that only admin user (neslihancekic) can see.

 .. code-block:: python

     def delete_tv(idno):
            try:
                with connection.cursor() as cursor:
                                statement = """DELETE FROM tvseries WHERE id=%s;"""                
                                cursor.execute(statement,(idno,))
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()

 .. code-block:: HTML

       {%if current_user.username=="neslihancekic"%}
                <div class="row">
                    <form action="" method="POST">
                        <button name="deletetv" value="1" class="btn btn-link btn-danger"><i class="ion-ios-film mr-2"></i>Delete {{tv.title}}</button>
                    </form>
                </div>
        {%endif%}

8. Add Episode Page
===================

This page is used to add episodes that aren't on that tvseries. To do this, episodeForm was created in the Forms.py file.

 .. code-block:: python

    class episodeForm(FlaskForm):
       title= StringField('Title',validators=[DataRequired()])
       season= IntegerField('Language',validators=[DataRequired()])
       episode= IntegerField('Year',validators=[DataRequired()])
       submit = SubmitField('Add Episode')

In the tvseries.py file, the season_check function allows you to check whether the entered season exists or not, and the episode_check function to check whether that episode exists in the database.
 
 .. code-block:: python

    def season_check(seas,idno):
       statement = """SELECT season FROM tvseries WHERE id=%s; """
       cursor.execute(statement,(idno,))
       season=cursor.fetchone()[0]
       if season>=seas:
           return True
       return False

  .. code-block:: python

        def episode_check(seas,ep,idno):
           a=0
           statement = """SELECT season_n,number,tvid FROM episode WHERE tvid=%s AND season_n=%s AND number=%s; """
           cursor.execute(statement,(idno, seas,ep))
           for check in cursor:
               a=a+1
           if a==0:
              return False
           return True

The insert operation is completed by writing the add_episode function.

 .. code-block:: python

    def add_episode(tvid,name,number,season_n):
       try:  
           with connection.cursor() as cursor:
               statement = """INSERT INTO episode (tvid, name, number, season_n)
                                        VALUES (%s, %s, %s, %s)
                                    RETURNING id;"""                
               cursor.execute(statement,(tvid,name,number,season_n))
               connection.commit()
               episode_id = cursor.fetchone()[0]
       except:
           connection.rollback()
           cursor=connection.cursor()  

The addepisode page has been built in server.py, paying attention to validations.

 .. code-block:: python

     @app.route("/tv/<int:item>", methods=['GET', 'POST']) #dynamic pages
     @login_required
     def tv(item):
    tv=find_tv(item)
    commit_list=print_commit(item)
    if request.method =='POST':
            try: 
                if request.form["fav"]=='1':
                        fav_add(current_user.id,item)
                        return redirect(url_for('tv',item=item))
            except:
                pass
            try: 
                if request.form["hate"]=='1':
                        hate_add(current_user.id,item)
                        return redirect(url_for('tv',item=item))
            except:
                pass
            try: 
                if request.form["wish"]=='1':
                        wish_add(current_user.id,item)
                        return redirect(url_for('tv',item=item))
            except:
                pass
            try:
                episodeid=request.form['episodeid']
                episodewatched(current_user.id,episodeid)
            except:
                pass
            try:
                if request.form["like_update"]=='1':
                    commitid=request.form['commitid']
                    com_like(commitid)
                    return redirect(url_for('tv',item=item))
            except:
                pass
            try:
                if request.form["submitcommit"]=='1':
                    tvid=request.form['tvidforcommit']
                    commith=request.form['header']
                    commitc=request.form['content']
                    submit_commit(tvid,current_user.id,commith,commitc)
                    return redirect(url_for('tv',item=item))
            except:
                pass
           
            try:
                if request.form["dislike_update"]=='1':
                    commitid=request.form['commitid']
                    com_dislike(commitid)
                    return redirect(url_for('tv',item=item))
            except:
                pass
        
            try:
                score=int(request.form['rate'])*2
                add_scoret(item,score)
                return redirect(url_for('tv',item=item))
            except:
                pass

            try:
                deletecommit=request.form['delete']
                delete_commit(deletecommit,current_user.id)
                return redirect(url_for('tv',item=item))
            except:
                pass
            try:
                if request.form['deletetv'] =='1':
                    delete_tv(item)
                    return redirect(url_for('tvpage',sort="sortbydefault"))
            except:
                pass

    return render_template("tv.html", tv=tv, commit=commit_list)


