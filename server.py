from flask import Flask,render_template,url_for
from userform import registirationForm, loginForm

import dbinit
import books, tvseries

app = Flask(__name__)

@app.route("/")
def home_page():
    
    return render_template("index.html")

@app.route("/home")

def h_page():
    return render_template("home.html")

@app.route("/signup")

def signup_page():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run()
