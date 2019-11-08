from flask import Flask,render_template,url_for,flash, redirect, request
from userform import registirationForm, loginForm

import dbinit
import books, tvseries

app = Flask(__name__)

app.config['SECRET_KEY'] = '41d1a759fd2a316f650e89fdb03e21d0'


@app.route("/")
def login_page():
    form=loginForm()
    return render_template("login.html", form = form)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/signup", methods=['GET', 'POST'])

def signup_page():
    form=registirationForm()
    if request.method =='POST':
        print(form.name.data,form.surname.data,form.username.data,form.mail.data,form.password.data)
        if form.validate_on_submit():
            flash(f'Account Created for {form.username.data}!', 'success')
            print('lol')
            return redirect(url_for('home'))
        else:
            
            flash(f'Mistake {form.username.data}!', 'warning')
            print('lol2')

    return render_template("signup.html", form=form)


if __name__ == "__main__":
    app.run()
