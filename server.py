from flask import Flask,render_template,url_for,flash, redirect, request
import dbinit
from tvseries import TV,print_tv,find_tv,seasonwatched,episodewatched, submit_commit, print_commit, com_like, com_dislike,fav_add,hate_add,wish_add,print_watching
from books import Book, print_book, find_book, updatepage,check_tpage, submit_commit_book,print_commit_book,com_like_book, com_dislike_book,fav_addb,hate_addb,wish_addb
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user, current_user, logout_user, login_required
from userdb import User, username_check, get
from forms import registirationForm, loginForm, tvForm, bookForm, UpdateForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '41d1a759fd2a316f650e89fdb03e21d0'
app.config['DATABASE_URL'] = 'postgres://dneperyi:l94XrLU-lOV2MOaQOPBnoYqVdKreucNZ@manny.db.elephantsql.com:5432/dneperyi'

bcrypt = Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view='login_page'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
    return get(int(user_id))


@app.route("/", methods=['GET', 'POST'])
def login_page():
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

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    watching_list=print_watching()
    if request.method =='POST':
        item=request.form['tv_id']
        return redirect(url_for('tv',item=item))
    return render_template("home.html",watching=watching_list)    

@app.route("/tv", methods=['GET', 'POST'])
@login_required
def tvpage():
    tv_list=print_tv()
    
    if request.method =='POST':
        try:
            item=request.form['form_id']
            return redirect(url_for('tv',item=item))
        except:
            tvid=request.form['tvid']
            season=request.form['sezon']
            seasonwatched(current_user.id,tvid,season)

    return render_template("tvpage.html", tv=tv_list)
    
@app.route("/tv/<int:item>", methods=['GET', 'POST']) #dynamic pages
@login_required
def tv(item):
    tv=find_tv(item)
    commit_list=print_commit(item,current_user.id)
    if request.method =='POST':
            try: 
                if request.form["fav"]=='1':
                        fav_add(current_user.id,item)
                        return redirect(url_for('tv',item=item))
            except:
                print("jjj")
            try: 
                if request.form["hate"]=='1':
                        hate_add(current_user.id,item)
                        return redirect(url_for('tv',item=item))
            except:
                print("jjj")
            try: 
                if request.form["wish"]=='1':
                        wish_add(current_user.id,item)
                        return redirect(url_for('tv',item=item))
            except:
                print("jjj")
            try:
                episodeid=request.form['episodeid']
                episodewatched(current_user.id,episodeid)
            except:
                print("ksf")
            try:
                if request.form["like_update"]=='1':
                    commitid=request.form['commitid']
                    com_like(commitid)
                    return redirect(url_for('tv',item=item))
            except:
                print("ksf")
            try:
                if request.form["submitcommit"]=='1':
                    tvid=request.form['tvidforcommit']
                    commith=request.form['header']
                    commitc=request.form['content']
                    submit_commit(tvid,current_user.id,commith,commitc)
                    return redirect(url_for('tv',item=item))
            except:
                print("ksf")
           
            try:
                if request.form["dislike_update"]=='1':
                    commitid=request.form['commitid']
                    com_dislike(commitid)
                    return redirect(url_for('tv',item=item))
            except:
                print("ksf")
        
            try:
                episodeid=request.form['episodeid']
                episodewatched(current_user.id,episodeid)
            except:
                print("ksf")
    return render_template("tv.html", tv=tv, commit=commit_list)


@app.route("/bookpage", methods=['GET', 'POST'])
@login_required
def bookpage():
    book_list=print_book() # BÜTÜN BOOK OBJELERİNİN ARRRAYİ
    if request.method =='POST':
        try:
            item=request.form['form_id']
            return redirect(url_for('book',item=item))
        except:
            readed=int(request.form['page'])
            bookid=request.form['bookid']
            if check_tpage(readed,bookid,current_user.id)==True:
                updatepage(bookid, current_user.id, readed)
            else:
                flash(f'Invalid Page Number!', 'danger')

    return render_template("bookpage.html", book=book_list) #book listi book adındA HTML E GÖNDERİYOR.

@app.route("/book/<int:item>", methods=['GET', 'POST']) #dynamic pages
@login_required
def book(item):
    book = find_book(item)
    commit_list=print_commit_book(item,current_user.id)
    if request.method =='POST':
        try:
                if request.form["like_update"]=='1':
                    commitid=request.form['commitid']
                    com_like_book(commitid)
                    return redirect(url_for('book',item=item))
        except:
                print("ksf")
                 
        try:
                if request.form["dislike_update"]=='1':
                    commitid=request.form['commitid']
                    com_dislike_book(commitid)
                    return redirect(url_for('book',item=item))
        except:
                print("ksf")
        
        try:
            if request.form["submitcommit"]=='1':
                    bookid=request.form['bookidforcommit']
                    commith=request.form['header']
                    commitc=request.form['content']
                    submit_commit_book(bookid,current_user.id,commith,commitc)
                    return redirect(url_for('book',item=item))
        except:
            print("jjj")
        try: 
            if request.form["fav"]=='1':
                    print("bebek")
                    fav_addb(current_user.id,item)
                    return redirect(url_for('book',item=item))
        except:
            print("jjj")
        try: 
            if request.form["hate"]=='1':
                    hate_addb(current_user.id,item)
                    return redirect(url_for('book',item=item))
        except:
            print("jjj")
        try: 
                if request.form["wish"]=='1':
                        wish_addb(current_user.id,item)
                        return redirect(url_for('book',item=item))
        except:
                print("jjj")
    return render_template("book.html", book=book, commit=commit_list)



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

@app.route("/addtv", methods=['GET', 'POST'])
@login_required
def tvform_page():
    form=tvForm()
    if request.method =='POST':
        if form.validate_on_submit:
            tv = TV(title=form.title.data,language=form.language.data, year=form.year.data,season=form.season.data,genre=form.genre.data,channel=form.channel.data)
            tv.addtv()
            flash(f'{form.title.data} is created!', 'success')
            return redirect(url_for('home'))
    return render_template("addtv.html", form = form)

@app.route("/addbook", methods=['GET', 'POST'])
@login_required
def bookForm_page():
    form=bookForm()
    if request.method =='POST':
        if form.validate_on_submit:
            print(form.name.data,form.writer.data)
            book = Book(name=form.name.data,writer=form.writer.data, year_pub=form.year_pub.data,tpage=form.tpage.data,publisher=form.publisher.data,language=form.language.data,genre=form.genre.data)
            book.addbook()
            flash(f'{form.name.data} is created!', 'success')
            return redirect(url_for('home'))
    return render_template("addbook.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route("/account")
@login_required
def account():
    form = UpdateForm()
    return render_template("account.html", current_user= current_user, form = form)

if __name__ == "__main__":
    app.run()
    