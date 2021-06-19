from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy # Use for Databasing in Future

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/stats")
def stats():
	return render_template("stats.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/register")
def register():
	return render_template("register.html")

if __name__ == "__main__":
	app.run(debug="True")

