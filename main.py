from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = "x{RD/'wutjN87mGN/acnEPSqkS4wp_"
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

        # Get User Input from HTML Form
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User(username=username, email=email, password=password)

        # Check to see username is already in use
        if User.query.filter_by(username=username).first() is not None:
            flash(f'Registration Unsuccessful. The username you have entered is already in use', 'danger')
            return render_template('register.html', title='Register', form=form)

        # Check to see if email address is already in use
        if User.query.filter_by(email=email).first() is not None:
            flash(f'Registration Unsuccessful. The email you have entered is already in use', 'danger')
            return render_template('register.html', title='Register', form=form)

        # Add user to database
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {username}!', 'success')

        # Create session for user
        session.permanent = True
        session["username"] = username

        flash(f'Registration Successful. Welcome, {username}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # Get User Input from HTML Form
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if Login Credentials are correct
        user = User.query.filter_by(email=email).first()
        if user is not None and form.email.data == user.email and form.password.data == user.password: 
            # Create session for user then redirect to home
            session.permanent = True
            session["username"] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    # Removes user from session and redirects to home
    if "username" in session:
        flash(f'Welcome back, {session["username"]}!', 'success')
        session.pop("username", None)
    return redirect(url_for("home"))


#############################################
### TEMPORARY ROUTES FOR TESTING PURPOSES ###
#############################################

# Temporary Route Made to See Entire Database
@app.route('/users')
def users():
    users = User.query.all()
    html = ''
    for user in users:
        html += f'''<div>Username: {user.username}</div>
                <div>Email: {user.email}</div>
                <div>Password:{user.password}</div>
                <div>----------------------------------------------</div>'''
    return html

# Temporary Route Made to Specific User in Database
@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return f'''<div>Username: {user.username}</div>
            <div>Email: {user.email}</div>
            <div>Password:{user.password}</div>
            <div>----------------------------------------------</div>'''

# Temporary Route to Clear Database
@app.route('/clear_users')
def clear_users():
    try:
        db.session.query(User).delete()
        db.session.commit()
        return "Success - Database cleared"
    except:
        return "Failed - Database not cleared"

if __name__ == '__main__':
    app.run(debug=True)
