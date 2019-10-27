from flask import Flask,render_template
import dbinit

app = Flask(__name__)

@app.route("/")
def home_page():
    a=dbinit.a()
    return render_template("index.html", lol2=a.name,lol=a.idd,lol3=a.ep)


if __name__ == "__main__":
    app.run()
