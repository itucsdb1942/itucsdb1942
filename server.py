from flask import Flask,render_template,url_for,flash, redirect, request
from tvseries import TV,print_tv
from books import Book, print_book
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user, current_user, logout_user
from userdb import User, username_check, get
from forms import registirationForm, loginForm, tvForm, bookForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '41d1a759fd2a316f650e89fdb03e21d0'
app.config['DATABASE_URL'] = 'postgres://dneperyi:l94XrLU-lOV2MOaQOPBnoYqVdKreucNZ@manny.db.elephantsql.com:5432/dneperyi'

bcrypt = Bcrypt(app)
login_manager= LoginManager(app)

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
                return redirect(url_for('home'))
            else:
                flash(f'Login Unsuccessful. Check Username and Password!', 'warning')
    return render_template("login.html", form = form)
    

@app.route("/home", methods=['GET', 'POST'])
def home():
    tv_list=print_tv()
    return render_template("home.html", tv=tv_list)
    

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
def account():
    
     return render_template("account.html")

if __name__ == "__main__":
    app.run()
    