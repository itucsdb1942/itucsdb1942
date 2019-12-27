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
.. example-code::
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

For the home page, functions were first written in the tvseries.py file and in the books.py file to print the lists. (The books.py file is made by my groupmate.) The functions in TVseries are print_watching, print_watched, print_wish, print_fav, print_hate. The sample code is given below.
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


Then a function named print_tv () was written to see all tvseries in the database.


Print_tv_by_az (), print_tv_by_score (), print_tv_by_year () functions were written for sort operations.

TV_percent method of TV class was created for the tvseries tracking progress.


A function named season_percent has been created for the progress of the specific season.


The seasonwatched function was written for the season watch button. Here, if the user has watched that season, the try except method was used to delete those lines.


The tvpage web page was created in the server.py file, and it was determined which sort order according to its extension.

When clicking on tvseries, the post method was used to redirect to its web page. Another post method was created for the season watch button.


In tvpage.html, a dropdown was created for sort operations.


The information of all the series was printed.


A hidden form was created to go to the dynamic page of any tvseries. Also, the tv_percent function has colored the icon of the tvseries according to the viewing status.

For the seasons, the loop was created and the buttons were functionalized with the form. With the season_percent function, the watch button was colored and a progress bar was made.


6. Add TV Series Page
=====================

This page is accessed via the button at the beginning of the tvpage./
A form class named tvForm was created in forms.py for adding tvseries to the database.


The addtv function has been added to the TV class in the tvseries.py file.


In server.py, the addtv page was created with the same logic as the sign up page. A redirect is provided to the home page if the operation is successful.


7. Dynamic Page of Tv Series
============================

First, the function named find_tv was written to tvseries.py to get the information of the tvseries with its id number./


I will explain the content of these dynamic pages that host many processes by categorizing them.

7.1. TV Series List Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tv_list is a boolean table that checks if a tvseries belongs to which list. In this table, which has a total of 5 lists (columns), the control operation is for one tvseries in one line. Therefore, update operation was applied instead of delete operation./
To add tvseries to the list, the functions fav_add, hate_add and wish_add were written to tv_series.py.


In addition, watched_add, watching_add, notwatch_add functions were written. Since they are related to each other, the update operations are performed accordingly.


Also check_fav, check_hate and check_wish functions were written to check if they are in the list. So if the TVseries is in that list the button is colored accordingly.

7.2. TV Series Episode Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, a class named Episode was created in the tvseries.py file.
CODE
In order to print the episodes of a season, the method called print_episode was written to the TV class.
CODE
The checkEpisodewatched method was written to check if the episode was watched.
CODE
The episodewatched function is written to save the episode to the database. If the episode is already watched, the code is entered in except and the episode is removed from the tv_trace table.
CODE

7.2. TV Series Comment Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For comments, a class named commit was created in tvseries.py.
CODE
A function named print_commit was written to see all comments in the database.
CODE
Com_like_number and com_dislike_number methods have been written to commit class to see how many dislike and dislike it takes.
CODE
The com_like and com_dislike update functions have been written to give comments like and dislike.
CODE
Submit_commit function was added to add a new comment.
CODE
The delete_commit function was written to delete the comment. The delete button is only displayed in the current user's comments.
CODE
HTML CODE

7.2. TV Series Vote Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The add_scoret function was written to tvseries.py to update the score.
CODE

7.2. TV Series Delete Operation (For Admin User)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A function named delete_tv has been created in tvseries.py for this option that only admin user (neslihancekic) can see.
CODE
HTML CODE

8. Add Episode Page
===================

This page is used to add episodes that aren't on that tvseries. To do this, episodeForm was created in the Forms.py file.
CODE
In the tvseries.py file, the season_check function allows you to check whether the entered season exists or not, and the episode_check function to check whether that episode exists in the database.
CODE
The insert operation is completed by writing the add_episode function.
CODE
The addepisode page has been built in server.py, paying attention to validations.
CODE
