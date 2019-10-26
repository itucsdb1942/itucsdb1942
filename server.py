from flask import Flask
import dbinit

app = Flask(__name__)


@app.route("/")
def home_page():
    
    print(35)
    return "Hello, world!"



if __name__ == "__main__":
    app.run()
