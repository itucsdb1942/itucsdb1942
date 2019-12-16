from flask import Flask,render_template,url_for,flash, redirect, request
import dbinit
from tvseries import TV,find_tv,seasonwatched,episodewatched,season_check,add_episode,episode_check,add_scoret
from tvseries import submit_commit, print_commit, com_like, com_dislike,delete_commit #commit operations
from tvseries import fav_add,hate_add,wish_add,print_watching,print_watched,print_wish,print_fav,print_hate #list operations
from tvseries import print_tv,print_tv_by_az,print_tv_by_score,print_tv_by_year #sort operations
from books import Book, find_book, updatepage,check_tpage,add_score
from books import print_book,print_book_by_az,print_book_by_score,print_book_by_year #sort operations
from books import submit_commit_book,print_commit_book,com_like_book, com_dislike_book, delete_commitb #commit operations
from books import print_favb,print_hateb,print_wishb,print_readed,print_reading,fav_addb,hate_addb,wish_addb #list operations
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user, current_user, logout_user, login_required
from userdb import User, username_check, get, update_user, delete_user
from forms import registirationForm, loginForm, tvForm, bookForm, UpdateForm, episodeForm

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

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    watching_list=print_watching(current_user.id)
    watched_list=print_watched(current_user.id)
    wish_list=print_wish(current_user.id)
    fav_list=print_fav(current_user.id)
    hate_list=print_hate(current_user.id)
    reading_list=print_reading(current_user.id)
    readed_list=print_readed(current_user.id)
    wishb_list=print_wishb(current_user.id)
    favb_list=print_favb(current_user.id)
    hateb_list=print_hateb(current_user.id
    )
    if request.method =='POST':
        try:
            item=request.form['tv_id']
            return redirect(url_for('tv',item=item))
        except:
            item=request.form['book_id']
            return redirect(url_for('book',item=item))
    return render_template("home.html",watching=watching_list,watched=watched_list,fav=fav_list,hate=hate_list,wish=wish_list,reading=reading_list,readed=readed_list,favb=favb_list,hateb=hateb_list,wishb=wishb_list)    


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

    return render_template("tv.html", tv=tv, commit=commit_list)

@app.route("/addepisode/<int:item>", methods=['GET', 'POST']) #dynamic pages
@login_required
def addepisode(item):
    tv=find_tv(item)
    form=episodeForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            check=season_check(form.season.data,item)
            check2=episode_check(form.season.data,form.episode.data,item)
            if check2:
                if check == True:
                    add_episode(item,form.title.data,form.episode.data,form.season.data)
                    flash(f'S{form.season.data}E{form.episode.data}:{form.title.data} added to {tv.title}!', 'success')
                    return redirect(url_for('addepisode',item=item))
                else:
                    flash(f'Invalid Season Number!', 'danger')
            else:
                flash(f'This episode already exist!', 'danger')
                

    return render_template("addepisode.html", form=form, tv=tv)

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

@app.route("/book/<int:item>", methods=['GET', 'POST']) #dynamic pages
@login_required
def book(item):
    book = find_book(item)
    commit_list=print_commit_book(item)
    if request.method =='POST':
        try:
                if request.form["like_update"]=='1':
                    commitid=request.form['commitid']
                    com_like_book(commitid)
                    return redirect(url_for('book',item=item))
        except:
                pass
                 
        try:
                if request.form["dislike_update"]=='1':
                    commitid=request.form['commitid']
                    com_dislike_book(commitid)
                    return redirect(url_for('book',item=item))
        except:
                pass
        
        try:
            if request.form["submitcommit"]=='1':
                    bookid=request.form['bookidforcommit']
                    commith=request.form['header']
                    commitc=request.form['content']
                    submit_commit_book(bookid,current_user.id,commith,commitc)
                    return redirect(url_for('book',item=item))
        except:
            pass
        try: 
            if request.form["fav"]=='1':
                    fav_addb(current_user.id,item)
                    return redirect(url_for('book',item=item))
        except:
            pass
        try: 
            if request.form["hate"]=='1':
                    hate_addb(current_user.id,item)
                    return redirect(url_for('book',item=item))
        except:
            pass
        try: 
                if request.form["wish"]=='1':
                        wish_addb(current_user.id,item)
                        return redirect(url_for('book',item=item))
        except:
                pass
        try:
            score=int(request.form['rate'])*2
            add_score(item,score)
            return redirect(url_for('book',item=item))
        except:
            pass
        try:
            deletecommit=request.form['delete']
            delete_commitb(deletecommit,current_user.id)
            return redirect(url_for('book',item=item))
        except:
            pass

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
            book = Book(name=form.name.data,writer=form.writer.data, year_pub=form.year_pub.data,tpage=form.tpage.data,publisher=form.publisher.data,language=form.language.data,genre=form.genre.data)
            book.addbook()
            flash(f'{form.name.data} is created!', 'success')
            return redirect(url_for('home'))
    return render_template("addbook.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route("/account", methods=['GET', 'POST'])
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

if __name__ == "__main__":
    app.run()
    