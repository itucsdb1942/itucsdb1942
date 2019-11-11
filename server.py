from flask import Flask,render_template,url_for,flash, redirect, request
import dbinit,books,tvseries
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user
from userdb import User, username_check, get
from userform import registirationForm, loginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '41d1a759fd2a316f650e89fdb03e21d0'
app.config['DATABASE_URL'] = 'postgres://dneperyi:l94XrLU-lOV2MOaQOPBnoYqVdKreucNZ@manny.db.elephantsql.com:5432/dneperyi'
bcrypt = Bcrypt(app)
login_manager= LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return get(int(user_id))

tv_list=tvseries.print_tv()

for item in tv_list:
    item.print()

@app.route("/", methods=['GET', 'POST'])
def login_page():
    form=loginForm()
    if request.method =='POST':
        if form.validate_on_submit:
            print("lol")
            user = username_check(form.username.data)
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
            else:
                print("lol2")
                flash(f'Login Unsuccessful. Check Username and Password!', 'warning')
    return render_template("login.html", form = form)
    

@app.route("/home")
def home():
    return render_template("home.html")

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


if __name__ == "__main__":
    app.run()
