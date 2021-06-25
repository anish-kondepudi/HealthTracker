from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg') # use hash
    password = db.Column(db.String(60), nullable=False) # use hash

    def __repr__(self) :
        return f"User('{self.username}','{self.email}')"


@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/stats")
def stats():
	return render_template("stats.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        # Add try and except to catch error of non-unique email/username
        flash(f'Account created for {username}!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Button pressed!")
        if form.email.data == 'admin@admin.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            # flash(f'Welcome back, {form.username.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Temporary Route Made to See Database
# @app.route('/get_users/<username>', methods=['GET'])
# def get_users():
#     user = User.query.filter_by(username=username).first()
#     return f'Username: {user.username}\nEmail: {user.email}\nPassword:{user.password}'

if __name__ == '__main__':
    app.run(debug=True)
