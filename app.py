from flask import Flask

app = Flask(__name__)

@app.route("/")
def Home():
    return "This is my restaurant API"


if __name__  == "__main__":
    app.run(debug=True)