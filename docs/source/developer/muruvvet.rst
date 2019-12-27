Parts Implemented by Mürüvvet BOZKURT
================================

**************
Creation of Tables
**************
.. note:: All table creations exist in db_init.py file.

We created a domain called scores to define score. All tables are created in "INIT_STATEMENTS"

.. code-block:: sql
	""" CREATE DOMAIN SCORES AS FLOAT
            DEFAULT 0.0
            CHECK((VALUE>=0.0) AND (VALUE<=10.0)); """

Firstly, I thought of all the tables I would use and created them. There are 3 main tables and 2 extra tables for books. My main tables are "books", "book_list", "comment_b" and my extra tables are "Writer" and "Book_trace". I do not need the "Writer" table, but I did not delete it because it would be hard to make changes because I started writing the code. The reason for "on delete cascade" addition will be explained in the account.py

.. code-block:: sql
	"""CREATE TABLE writer(
            ID SERIAL PRIMARY KEY,
            wr_name VARCHAR(50) NOT NULL UNIQUE,
            wr_country VARCHAR(50)
        );""",

         """ CREATE TABLE books(
            ID SERIAL PRIMARY KEY,
            NAME VARCHAR(80) UNIQUE NOT NULL,
            WRITERID INTEGER REFERENCES writer(id),
            PUB_YEAR INTEGER,
            T_PAGE INTEGER,
            PUBLISHER VARCHAR(50),
            LANGUAGE VARCHAR(80),
            GENRE VARCHAR(50),
            SCORE SCORES,
            VOTE INTEGER DEFAULT 0);""",

        """CREATE TABLE book_list(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id) on delete cascade,
            bookid INTEGER REFERENCES books(id) on delete cascade,
            fav_b BOOL DEFAULT FALSE,
            hate_b BOOL DEFAULT FALSE,
            wish_b BOOL DEFAULT FALSE,
            readed BOOL DEFAULT FALSE,
            reading BOOL DEFAULT FALSE,
            UNIQUE(userid,bookid)
        );""",

        """CREATE TABLE book_trace(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id) on delete cascade,
            bookid INTEGER REFERENCES books(id) on delete cascade,
            readpage INTEGER DEFAULT 0,
            UNIQUE(userid, bookid)
        );""",

        """CREATE TABLE comment_b(
            ID SERIAL PRIMARY KEY,
            userid INTEGER REFERENCES users(id) on delete cascade,
            bookid INTEGER REFERENCES books(id) on delete cascade,
            headerb VARCHAR(30),
            contentb VARCHAR(250),
            likeb INTEGER DEFAULT 0,
            dislikeb INTEGER DEFAULT 0,
            date TIMESTAMP
        );"""


****************
books.py
****************

1. Basic Book Operations
~~~~~~~~~~~~~~~~~~~~~~~~
Basic book operations contain functions for printing information of the one book(dynamic page), deleting books, checking progress, updating page number that user read and rating operations.

1.1 Printing Information of The One Book
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function returns one book. It provide us to print information of the book in dynamic page.

.. code-block:: python

     def find_book(idno):
        
                statement = """SELECT books.ID, books.NAME, writer.wr_name, books.PUB_YEAR, books.T_PAGE, books.PUBLISHER, 
                books.LANGUAGE, books.GENRE, books.SCORE, books.VOTE FROM BOOKS, writer WHERE books.id=%s AND books.writerid=writer.id; """
                cursor.execute(statement,(idno,))
                connection.commit()
                for id, name, wri_name, year, page, pub, lang, gen, sc, vote in cursor:
                    book =Book(id,name,wri_name,year,page,gprint_commit_booken,pub,lang,vote,sc)
                return book
         

1.2 Updating Page Number
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

1.3 checking Progress
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
    
1.4 Rate Book
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


1.5 Delete books
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

2. Sort Operations 
~~~~~~~~~~~~~~~~~~~~~~~~
These are the functions that determine the order in which books are printed on the book page.

2.1 Print Default & A-Z & Year & Score 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
         


3. Comment Operations
~~~~~~~~~~~~~~~~~~~~~~~~

3.1 Inserting
~~~~~~~~~~~
.. code-block:: python

 
