from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import timedelta, datetime

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
    stats = db.relationship('Stats', backref='author', lazy=True)

    def __repr__(self) :
        return f"User('{self.username}','{self.email}','{self.image}')"

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    overall_feeling = db.Column(db.Integer, nullable=False)
    time_slept = db.Column(db.Float, nullable=False)
    worked_out = db.Column(db.Boolean, nullable=False)
    ate_healthy = db.Column(db.String(100), nullable=False)
    time_worked_out = db.Column(db.Integer, nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)
    unhealthy_food = db.Column(db.String(500), nullable=False)
    proud_achievement = db.Column(db.String(2000), nullable=False)

    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/stats")
def stats():
    if "username" not in session:
        return redirect(url_for('home'))
    return render_template("stats.html")

@app.route("/log_data", methods=['GET', 'POST'])
def log_data():
    # If user is not logged in, redirect to home
    if "username" not in session:
        return redirect(url_for('home'))

    # Fires when submit button is pressed
    if request.method == 'POST':

        # Get User Input from HTML Form
        feeling = int(request.form.get('feeling'))
        sleep = float(request.form.get('sleep'))
        worked_out = bool(int(request.form.get('workout')))
        ate_healthy = request.form.get('healthy')
        proud_achievement = request.form.get('proudAchievement')
        time_worked_out = 0 # Default Value - If User did not Workout
        workout_type = "None" # Default Value - If User did not Workout
        unhealthy_food = "None" # Default Value - If User ate Healthy

        # Get workout info if user has worked out
        if (worked_out):
            time_worked_out = int(request.form.get('workoutTime'))
            if len(request.form.getlist('workoutType')) == 0: workout_type = "None"
            else: workout_type = ', '.join(request.form.getlist('workoutType'))

        # Get unhealthy food info if user did not eat healthy
        if (ate_healthy != "Yes"):
            unhealthy_food = request.form.get('unhealthyFood')

        # Edge case handling
        if (len(proud_achievement) == 0): proud_achievement = "None"
        if (len(unhealthy_food) == 0): unhealthy_food = "None"

        user = User.query.filter_by(username=session["username"]).first()

        stats = Stats(overall_feeling=feeling,
                    time_slept=sleep,
                    worked_out=worked_out,
                    ate_healthy=ate_healthy,
                    time_worked_out=time_worked_out,
                    workout_type=workout_type,
                    unhealthy_food=unhealthy_food,
                    proud_achievement=proud_achievement,
                    user_id=user.id,)

        # add conditional to check if data created is not today!

        # db.session.add()
        # db.session.commit()

        flash(f'Entry successfully added!', 'success')
        return redirect(url_for('stats'))

    return render_template("log_data.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to home
    if "username" in session:
        return redirect(url_for('home'))

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
    # If user is already logged in, redirect to home
    if "username" in session:
        return redirect(url_for('home'))

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
    stats = Stats.query.get_or_404(1)
    return f'''<div>Username: {user.username}</div>
            <div>Email: {user.email}</div>
            <div>Password:{user.password}</div>
            <div>Stats:{stats}</div>
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
