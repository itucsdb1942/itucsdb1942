Parts Implemented by Mürüvvet BOZKURT
=====================================
This page will be providing information on
* *Creation of Tables*
* *Basic Book Operations*
* *Book Sort Operations *
* *Book Comment Operations*
* *Book List Operations*
* *Add Book Page Operations*
* *Login Page Operations*
* *Account Operations*

Creation of Tables
-------------------


.. figure:: dbmur.png
	:scale: 30 %
	:alt: Database implemented by Mürüvvet
	:align: center

.. note:: All table creations exist in dbinit.py file.


Firstly, I thought of all the tables I would use and created them. There are 3 main tables and 2 extra tables for books. My main tables are "books", "book_list", "comment_b" and my extra tables are "Writer" and "Book_trace". I do not need the "Writer" table, but I did not delete it because it would be hard to make changes because I started writing the code. The reason for "on delete cascade" addition will be explained in the account.py

.. code-block:: sql

	CREATE TABLE writer(
            ID SERIAL PRIMARY KEY,
            wr_name VARCHAR(50) NOT NULL UNIQUE,
            wr_country VARCHAR(50)
        );,

          CREATE TABLE books(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(80) UNIQUE NOT NULL,
            WRITERID INTEGER REFERENCES writer(id),
            PUB_YEAR INTEGER,
            T_PAGE INTEGER,
            PUBLISHER VARCHAR(50),
            LANGUAGE VARCHAR(80),
            GENRE VARCHAR(50),
            SCORE SCORES,
            VOTE INTEGER DEFAULT 0);,

        CREATE TABLE book_list(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id) on delete cascade,
            bookid INTEGER REFERENCES books(id) on delete cascade,
            fav_b BOOL DEFAULT FALSE,
            hate_b BOOL DEFAULT FALSE,
            wish_b BOOL DEFAULT FALSE,
            readed BOOL DEFAULT FALSE,
            reading BOOL DEFAULT FALSE,
            UNIQUE(userid,bookid)
        );,

        CREATE TABLE book_trace(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id) on delete cascade,
            bookid INTEGER REFERENCES books(id) on delete cascade,
            readpage INTEGER DEFAULT 0,
            UNIQUE(userid, bookid)
        );,

        CREATE TABLE comment_b(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id) on delete cascade,
            bookid INTEGER REFERENCES books(id) on delete cascade,
            headerb VARCHAR(30),
            contentb VARCHAR(250),
            likeb INTEGER DEFAULT 0,
            dislikeb INTEGER DEFAULT 0,
            date TIMESTAMP
        );



Basic Book Operations
----------------------

Basic book operations contain functions for printing information of the one book(dynamic page), deleting books, checking progress, updating page number that user read and rating operations.

The books.py file was first created for the database operations of the book page. In this file, a class named "Book" has been created.

.. code-block:: python

	class Book:
    		def __init__(self, id=None, name=None, writer=None,year_pub=None,tpage=None,genre=None,publisher=None, language=None,vote=None,score= None):
        		self.id = id
        		self.name= name
        		self.writer= writer
        		self.year_pub= year_pub
        		self.tpage= tpage
        		self.genre= genre
        		self.publisher= publisher 
        		self.language= language 
        		self.vote=vote 
        		self.score=score

* *Printing Information of The One Book*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function returns one book. It provide us to print information of the book in dynamic page.

.. code-block:: python

	def find_book(idno):
        
                statement = """SELECT books.ID, books.NAME, writer.wr_name, books.PUB_YEAR, books.T_PAGE, books.PUBLISHER, 
                books.LANGUAGE, books.GENRE, books.SCORE, books.VOTE FROM BOOKS, writer WHERE books.id=%s AND books.writerid=writer.id; 		"""
                cursor.execute(statement,(idno,))
                connection.commit()
                for id, name, wri_name, year, page, pub, lang, gen, sc, vote in cursor:
                    book =Book(id,name,wri_name,year,page,gprint_commit_booken,pub,lang,vote,sc)
                return book

* *Updating Page Number*
~~~~~~~~~~~~~~~~~~~~~~~~

 The user can update the number of pages read with this function. The userid and bookid are unique because a book cannot be in the read list, read list, read list at the same time. If you take "UniqueViolation error, you update the number of pages of that book instead of inserting the same book to trace.

.. code-block:: python

	def updatepage(bookid, userid, page):
    
        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO book_trace (userid, bookid, readpage)
                            VALUES ( %s, %s, %s)
                        RETURNING id;"""
                cursor.execute(statement,(userid,bookid,page,))
                connection.commit()
        except dbapi2.errors.UniqueViolation:
            connection.rollback()
            with connection.cursor() as cursor:
                statement = """ UPDATE book_trace 
                            SET readpage = %s WHERE userid = %s AND bookid = %s"""
                cursor.execute(statement, (page, userid, bookid,))
                connection.commit()
        except dbapi2.errors.InFailedSqlTransactions:
            connection.rollback()
            cursor=connection.cursor()
	    
	
* *Checking Progress*
~~~~~~~~~~~~~~~~~~~~~~~~

This code does not allow entering a page number greater than the total page of the book.

.. code-block:: python

	def check_tpage(readed,bookid,userid):
                
                        statement="""SELECT t_page FROM books WHERE id= (%s)"""
                        cursor.execute(statement,(bookid,))
                        tpage=cursor.fetchone()[0] 
                        connection.commit() 
                        if readed>tpage:
                            return False
                        return True
    
* *Rate Book*
~~~~~~~~~~~~~~~~~~~~~~~~

This code will update the book's score and the number of times the book is rated.

.. code-block:: python

    def add_score(bookid,score):
    with connection.cursor() as cursor:
        statement = """ UPDATE books
                                SET SCORE = (SCORE*VOTE+%s)/(VOTE+1),VOTE=VOTE+1 WHERE id = %s;"""
        cursor.execute(statement, (score, bookid,))
        connection.commit()   
        cursor.close()  


* *Delete books*
~~~~~~~~~~~~~~~~~~~~~~~~

Only admin user can delete books. Since many tables are connected to userid and bookid, variables are defined in tables as cascading where necessary.

.. code-block:: python

          def delete_book(idno):
            try:
                with connection.cursor() as cursor:
                                statement = """DELETE FROM books WHERE id=%s;"""                
                                cursor.execute(statement,(idno,))
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()

Book Sort Operations 
----------------------

The bookpage web page was created in the server.py file, and it was determined which sort order according to its extension. When clicking on "books", the post method was used to redirect to its web page.

.. code-block:: python

	@app.route("/bookpage/<string:sort>", methods=['GET', 'POST'])
	@login_required
	def bookpage(sort):
    		book_list=print_book() # BÜTÜN BOOK OBJELERİNİN ARRRAYİ
    		if sort=="sortbyaz":
        		books=print_book_by_az()
    		elif sort=="sortbyscore":
        		books=print_book_by_score()
    		elif sort=="sortbyyear":
        		books=print_book_by_year()
    		elif sort=="sortbydefault":
        		books=print_book()
    		if request.method =='POST':
        	try:
            		item=request.form['form_id']
            		return redirect(url_for('book',item=item))
        	except:
            		pass
        	try:
            		readed=int(request.form['page'])
           		 bookid=request.form['bookid']
            		if check_tpage(readed,bookid,current_user.id)==True:
                		updatepage(bookid, current_user.id, readed)
            		else:
                		flash(f'Invalid Page Number!', 'danger')
        	except:
            		pass
       
    return render_template("bookpage.html", book=books) #book listi book adındA HTML E GÖNDERİYOR.
		
These are the functions that determine the order in which books are printed on the book page.

* *Print Default & A-Z & Year & Score* 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These functions sort by book id, alphabetical order, year, score. The only difference between functions is the "ORDER BY..." part. Book_list is a tuble that contains all books. We add each book in our database to this tuple. In fact,  tuple is printed on the screen. 

For Example:

Print Default

.. code-block:: python

     def print_book():
                with connection.cursor() as cursor:
                    book_list=[]
                    statement = """SELECT books.ID, books.NAME, writer.wr_name, books.PUB_YEAR, books.T_PAGE, books.PUBLISHER, 
                    books.LANGUAGE, books.GENRE, books.SCORE, books.VOTE FROM BOOKS, writer WHERE books.writerid=writer.id ORDER BY id; """
                    cursor.execute(statement)
                    for id, name, wr_name, year, page, pub, lang, gen, sc, vote in cursor:
                            book =Book(id,name,wr_name,year,page,gen,pub,lang,vote,sc)
                            book_list.append(book)
                    connection.commit()
                    return book_list
         

Book Comment Operations
--------------------------- 

For comments, a class named commitb was created in books.py.

.. code-block:: python
	
	class commitb:
    		def __init__(self,id=0,username=0,bookid=0,header=0,content=0,date=0,like=0,dislike=0):
       			self.id=id
        		self.username=username
        		self.bookid=bookid
        		self.header=header
        		self.content=content
        		self.date=date
        		self.like=like
        		self.dislike=dislike

* *Inserting*
~~~~~~~~~~~~~~~

You add a new row to the comment table by adding a comment. Datetime.now provides that get the current date and time.

.. code-block:: python

	def submit_commit_book(bookid,userid,header,context):
            now = datetime.now()
            try:
                with connection.cursor() as cursor:
                                statement = """INSERT INTO comment_b (userid, bookid, headerb, contentb,date)
                                            VALUES (%s, %s, %s, %s, %s)
                                        RETURNING id;"""                
                                cursor.execute(statement,(userid,bookid,header,context,now))
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()

* *Deleting*
~~~~~~~~~~~~~

I enabled the user to delete only his / her comment by sending userid.

.. code-block:: python

	def  delete_commitb(idno, userid):
    try:
        with connection.cursor() as cursor:
                    statement = """ DELETE FROM comment_b 
                                WHERE userid = %s AND id = %s"""
                    cursor.execute(statement, ( userid, idno,))
                    connection.commit()
    except:
        connection.rollback()
        cursor=connection.cursor()

* *Updating and Reading Like & Dislike*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We send form to html and if like button is pressed it increases the number of likes by one. A user may like or dislike same comment more than once.To prevent this, I had to keep the userid, but it is not necessary, so I did not it.

.. code-block:: python

	def com_like_book(commitid):
            statement = """ UPDATE comment_b
                        SET likeb= likeb+1 WHERE id = %s;"""
            cursor.execute(statement, ( commitid,))
            connection.commit()
        
For reading numbers of like and dislike;

.. code-block:: python

	def com_dislike_numberb(self):
                statement = """ SELECT dislikeb FROM comment_b
                            WHERE  id = %s;"""
                cursor.execute(statement, (  self.id,))
                dislike_n=cursor.fetchone()[0]
                connection.commit()
                return dislike_n
	


        

* *Reading*
~~~~~~~~~~~~~~~~~~

I added all comments to the commit list and returned the commit list. So I wrote the required function to print all comments on the screen.

.. code-block:: python

	def print_commit_book(bookid):
            commits=[]
            try:
                with connection.cursor() as cursor:
                                statement = """SELECT comment_b.id, comment_b.headerb,comment_b.contentb,comment_b.date, users.username FROM comment_b,users
                                             WHERE comment_b.bookid=(%s) AND comment_b.userid=users.id ORDER BY date DESC;"""                
                                cursor.execute(statement,(bookid,))
                                for id,head,cont,date,username in cursor:
                                    com=commitb(id=id, username=username,bookid=bookid,header=head,content=cont,date=date)
                                    commits.append(com)  
                                
                                connection.commit()
            except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor()
                  
            return commits

Book List Operations
--------------------------

List operations consist of create, update, read operations.The values ​​stored in the list are in bool. 
When we want to remove a book from a list, we can not delete it. Because the deletion is done row by row and then the book is deleted from the other lists.  
In order to avoid this situation, I am just updating the table that user wants to add or remove.

* *Automatically Add to Some Lists*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function provide to add automatically to Read, Unread, reading list as percent progress of book.

.. code-block:: python

	def book_percent(self,userid):
                        connection.rollback()
                        cursor=connection.cursor()
                        checkreaded=0
                        statement="""SELECT readpage FROM book_trace WHERE bookid= (%s) AND userid=(%s)"""
                        cursor.execute(statement,(self.id,userid,))
                        for p in cursor:
                            checkreaded=p
                        if(checkreaded == 0):
                            return 0
                        connection.commit()
                        per=checkreaded[0]
                        percent=per*100/self.tpage
                        if(percent==100.0):
                            readed_add(userid,self.id)
                        elif(percent>0.0):
                            reading_add(userid,self.id)
                        elif(percent==0.0):
                            notread_add(userid,self.id)
                        return round(percent,2)
			
* *Checking Lists*
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

 	def check_hate(self,userid):
                connection.rollback()
                try:
                    with connection.cursor() as cursor:
                        statement = """ SELECT hate_b FROM book_list
                                    WHERE userid = %s AND bookid = %s;"""
                        cursor.execute(statement, ( userid, self.id,))
                        connection.commit()
                        check=cursor.fetchone()[0]
                        if check==False:
                            return False
                        return True
                except:
                    return False

* *Reading Lists*
~~~~~~~~~~~~~~~~~~~~~~

There are separate "read" functions for all tables in "book_trace". They all have the same structure. I've just changed which table to do. So here's just one example. 

.. code-block:: python

	def print_readed(idno):
    books={}
    try:
        with connection.cursor() as cursor:
                                statement = """SELECT book_list.bookid, books.name FROM book_list,books
                                             WHERE book_list.readed=TRUE AND book_list.bookid=books.id AND userid=%s;"""                
                                cursor.execute(statement,(idno,))
                                for bookid, bookname in cursor:
                                    books[bookid]=bookname
                                return books
    except dbapi2.DatabaseError:
                connection.rollback()
                cursor=connection.cursor() 

* *Adding Books to the Favorite, Hate, Wish list* 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The structure of functions of adding to favorite, wish or hate lists is the same. I implemented the same function for 3 separate lists.Therefore, there is only one code example below. If there is a "UniqueViolation", existing books are updated as true or false. If there is "InFailedSqlTransactions", a transaction goes back.

.. code-block:: python

	def fav_addb(userid,bookid):
        	try:
            	with connection.cursor() as cursor:
                	statement = """INSERT INTO book_list (userid, bookid, fav_b)
                            	VALUES ( %s, %s, %s)
                        	RETURNING id;"""
                	cursor.execute(statement,(userid,bookid,"TRUE"))
                	connection.commit()
                
        	except dbapi2.errors.UniqueViolation:
            	connection.rollback()
            
            	a="FALSE"
            	with connection.cursor() as cursor:    
                	statement = """ SELECT fav_b FROM book_list
                            	WHERE userid = %s AND bookid = %s;"""
                	cursor.execute(statement, ( userid, bookid,))
                	check=cursor.fetchone()[0]
                	if check == False:
                    		a="TRUE"
                	statement = """ UPDATE book_list 
                            	SET fav_b = %s WHERE userid = %s AND bookid = %s"""
                	cursor.execute(statement, (a, userid, bookid,))
                	connection.commit()
        	except dbapi2.errors.InFailedSqlTransactions:
            		connection.rollback()
            		cursor=connection.cursor()

Add Book Page Operations
--------------------------

This page is accessed via the button at the beginning of the book page.

A form class named BookForm was created in forms.py for adding books to the database.

.. code-block:: python
	
	class bookForm(FlaskForm):
    		name= StringField('Title',validators=[DataRequired()])
    		writer = StringField('Author',validators=[DataRequired()])
    		year_pub = DecimalField('Year of Publication',validators=[DataRequired()])
    		tpage = DecimalField('Total Page',validators=[DataRequired()])
    		publisher = StringField('Publisher',validators=[DataRequired()])
    		language = StringField('Language',validators=[DataRequired()])
    		genre = StringField('Genre',validators=[DataRequired()])
    		submit = SubmitField('Add Book')

The addbook function has been added to the Book class in the books.py file.

.. code-block:: python

	def addbook(self):
        writer_ids={}
        try:
            with connection.cursor() as cursor:
                wri_name = self.writer
                statement = """SELECT id FROM writer WHERE wr_name= (%s);"""
                cursor.execute(statement,(wri_name,))
                connection.commit()
                writer_id = cursor.fetchone()[0]   
                writer_ids[wri_name]=writer_id
        except dbapi2.DatabaseError:
            connection.rollback()
            cursor=connection.cursor()
        

        try:
            with connection.cursor() as cursor:
                wri_name = self.writer
                statement = """INSERT INTO writer (wr_name) VALUES (%s)
                                        RETURNING id;"""
                        
                cursor.execute(statement,(wri_name,))
                connection.commit()
                writer_id = cursor.fetchone()[0]   
                writer_ids[wri_name]=writer_id
        except dbapi2.DatabaseError:
            connection.rollback()
            cursor=connection.cursor()
        

        try:
            with connection.cursor() as cursor:
                statement = """INSERT INTO books (NAME, WRITERID, PUB_YEAR, T_PAGE, PUBLISHER, LANGUAGE, GENRE, SCORE, VOTE)
                                    VALUES (%s,%s,%s, %s,%s,%s,%s,%s,%s)
                            RETURNING id;"""
                cursor.execute(statement, (self.name, writer_ids[self.writer], self.year_pub, self.tpage, self.publisher, self.language, self.genre, self.score, self.vote))
                connection.commit()
                book_id = cursor.fetchone()[0]
        except dbapi2.DatabaseError:
            connection.rollback()
            cursor=connection.cursor()

A redirect is provided to the home page if the operation is successful in server.py 

.. code-block:: python

	@app.route("/addbook", methods=['GET', 'POST'])
	@login_required
	def bookForm_page():
    		form=bookForm()
    		if request.method =='POST':
        		if form.validate_on_submit:
            			book = Book(name=form.name.data,writer=form.writer.data, 	year_pub=form.year_pub.data,tpage=form.tpage.data,publisher=form.publisher.data,language=form.language.data,genre=form.genre.data)
            		book.addbook()
            		flash(f'{form.name.data} is created!', 'success')
            	return redirect(url_for('home'))
    		return render_template("addbook.html", form = form)

Login Page Operations
----------------------------

"@login_required"  does not provide access to some pages on the website without user input.
If the user input is correct, you will be redirected directly to the homepage.

.. code-block:: python

	@app.route("/", methods=['GET', 'POST'])
	def login_page():
    		if current_user.is_authenticated:
         		return redirect(url_for('home'))
    		form=loginForm()
    		if request.method =='POST':
        		if form.validate_on_submit:
            			user = username_check(form.username.data)
            			if user and bcrypt.check_password_hash(user.password,form.password.data):
                			login_user(user, remember=form.remember.data)
                			next_page=request.args.get('next')
                			return redirect(next_page) if next_page else redirect(url_for('home'))
            			else:
                			flash(f'Login Unsuccessful. Check Username and Password!', 'warning')
    		return render_template("login.html", form = form)
		
Flask_wtf was used to get inputs easily. To do this, a forms.py file was created and a class named loginnForm was created.
There is the validations of the information required for the user logining. Email and usename field can not be empty. Username and mail check functions are in userdb.py.

.. code-block:: python

	class loginForm(FlaskForm):
    		username =StringField('Username', validators=[DataRequired()])
    		password = PasswordField('Password', validators=[DataRequired()])
    		remember = BooleanField('Remember Me')
    		submit = SubmitField('Login')

These python code snippets check whether the username and mail address entered match the database.

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
		    

.. code-block:: python

	def mail_check(mail):
            with connection.cursor() as cursor:
                    statement = """SELECT id, name, surname, username, mail, gender, birth, password FROM users 
                                        WHERE mail = (%s); """
                    cursor.execute(statement,(mail,))
                    user= False
                    for i, n, s, u, m, g, b, p  in cursor:
                        user= User(id=i, name=n, surname=s, username=u,
                        mail=m, gender=g, date=b, password=p)
                    return user
            

Account Operations
----------------------
By implementing this function, the user registered in the web site can update this information with a user name and e-mail address that has not been received before.

.. code-block:: python

	def update_user(username,mail,id):
    		with connection.cursor() as cursor:
                    		statement = """UPDATE users SET mail = (%s), username=(%s) WHERE id=(%s); """
                    		cursor.execute(statement,(mail,username,id))

This is a python function for deleting the user from the database.Since the userid is linked to many tables, the userid and bookid, which are foreign key in some tables, are initially defined as "on delete cascade".

.. code-block:: python

	def delete_user(idno):
    		with connection.cursor() as cursor:
                    		statement = """DELETE FROM users WHERE id=(%s) ;
                                         """
                    		cursor.execute(statement,(idno,))
                    		connection.commit()

		@app.route("/account", methods=['GET', 'POST'])
		
if delete button is pressed, "1" value is sent from html form and user is deleted. you will be redirected to the login page. If the user has been updated, you will be redirected to your account page and you will see your updated data. These routing operations take place in the server.py file.
		
.. code-block:: python
		
	@login_required
	def account():
    		form = UpdateForm()
    		if request.method =='POST':
        		if request.form['delete']=='1':
            			delete_user(current_user.id)
            			logout_user()
            			return redirect(url_for('login_page'))
        		else:
            			if form.validate_on_submit():
                			update_user(form.username.data,form.mail.data,current_user.id)
               				flash(f'Updated Account: {form.username.data}, {form.mail.data}!', 'success')
                			return redirect(url_for('account'))
            	else:
                	flash(f'Failed to Update Account to {form.username.data}, {form.mail.data}!', 'danger')

    		return render_template("account.html", current_user= current_user, form = form)



 
