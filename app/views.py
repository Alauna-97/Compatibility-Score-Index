"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, login_manager
from flask_mysqldb import MySQL
from flask import render_template, request, redirect, url_for, flash, session
from app.forms import LoginForm, SignUp, Groupings, newSet, joinNewSet, AboutYou
from werkzeug.security import check_password_hash

import random
import uuid
# import mysql.connector
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     database="csi2"
# )

# mycursor = mydb.cursor()

###
# Routing for your application.
###

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'csi2'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if 'logged_in' in session:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        mycursor = mysql.connection.cursor()
        username = form.username.data
        # Query if User exists
        mycursor.execute(
            'SELECT * FROM user WHERE username = %s AND password = %s', (username, form.password.data,))
        user = mycursor.fetchone()
        print(user)

        # If existing user
        if user:
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['id'] = user['user_id']
            session['username'] = request.form['username']
            session['TYPE'] = user['type']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']

            # Flash Success
            flash('Login Successful', 'success')

            return redirect(url_for('dashboard', username=username))

        # Flash error message with incorrect username/password
        flash(u'Invalid Credentials', 'error')
    return render_template("login.html", form=form)


@app.route('/dashboard/<username>')
def dashboard(username):
    """Render the website's dashboard page."""
    if 'username' in session:
        mycursor = mysql.connection.cursor()
        mycursor.execute('Select * from user where username = %s', (username,))
        user = mycursor.fetchone()

        if session.get('TYPE') == "Organizer":
            mycursor.execute(
                'SELECT * FROM sets WHERE organizer = %s ', (session['id'],))
        else:
            mycursor.execute(
                'SELECT * FROM Sets JOIN joinset ON sets.sid = joinset.sid WHERE joinset.user_id = %s ', (session['id'],))
        getSets = mycursor.fetchall()
    return render_template('dashbrd.html', groups=getSets, type=session.get('TYPE'))


@app.route("/logout")
def logout():
    # Logout the user and end the session
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('type', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    flash('Logged out Succesfully', 'success')
    return redirect(url_for('home'))


@app.route('/registerAs', methods=["GET", "POST"])
def registerAs():
    """Render the website's register page."""
    if request.method == "POST":
        if request.form.get('Regular') == 'Regular':
            return redirect(url_for('register', typeUser="Regular"))

        elif request.form.get('Organizer') == 'Organizer':
            return redirect(url_for('register', typeUser="Organizer"))
    return render_template('registerAs.html')


@app.route('/register/<typeUser>', methods=["GET", "POST"])
def register(typeUser):
    # First Name, Last Name, Email, Password and Username are collected from the SignUp Form
    form = SignUp()

    if request.method == "POST" and form.validate_on_submit():
        mycursor = mysql.connection.cursor()
        # Collects username and email info from form
        username = form.username.data
        email = form.email.data

        # Checks if another user has this username
        mycursor.execute(
            'SELECT * FROM user WHERE username = %s', (username,))
        existing_username = mycursor.fetchone()

        # Checks if another user has this email address
        mycursor.execute(
            'SELECT * FROM user WHERE email = %s', (email,))
        existing_email = mycursor.fetchone()

        # Gets last record in User Table
        mycursor.execute(
            'SELECT * from user ORDER BY user_id DESC LIMIT 1')
        lastRec = mycursor.fetchone()
        if lastRec is None:
            lastRec = 1
        else:
            lastRec = lastRec['user_id'] + 1

        # If unique email address and username provided then log new user
        if existing_username is None and existing_email is None:
            mycursor = mysql.connection.cursor()
            sql = "INSERT INTO User (user_id, type, first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (lastRec, typeUser, request.form['fname'], request.form['lname'],
                   request.form['username'], request.form['email'], request.form['password'])

            mycursor.execute(sql, val)
            mysql.connection.commit()

            last = mycursor.lastrowid
            # Specialisation of Users
            if typeUser == "Regular":
                # Calls RandomFeatures  function to generate features for regular user
                randFt = randomFeatures()

                sql = "INSERT INTO Regular (user_id, gender, age, height, leadership, ethnicity, personality, education, hobby, occupation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (mycursor.lastrowid, randFt[0], randFt[1],
                       randFt[2], randFt[3], randFt[4], randFt[5], randFt[6], randFt[7], randFt[8])

                mycursor.execute(sql, val)
                mysql.connection.commit()

            else:
                position = random.choice(
                    ['Secretary', 'CEO', 'Treasurer', 'Vice President', 'Supervisor', 'Manager'])

                sql = "INSERT INTO Organizer (user_id, position) VALUES (%s, %s)"
                val = (mycursor.lastrowid, position)

                mycursor.execute(sql, val)
                mysql.connection.commit()

            # Success Message Appears
            flash('Successfully registered', 'success')

            # Logs in a newly registered user
            session['logged_in'] = True
            session['id'] = last
            session['username'] = request.form['username']
            session['TYPE'] = typeUser
            session['first_name'] = request.form['fname']
            session['last_name'] = request.form['lname']

            # Redirects to Profile Page
            return redirect(url_for('dashboard', username=session.get('username')))

    # Flash errors in form and redirects to Register Form
    flash_errors(form)
    return render_template("signup.html", form=form)


@app.route('/<username>/createSet',  methods=['GET', 'POST'])
def createSet(username):
    """Render the website's page."""
    form = newSet()
    # If user is logged in session and is an organizer
    if 'username' in session and session.get('TYPE') == "Organizer":
        mycursor = mysql.connection.cursor()
        if request.method == "POST" and form.validate_on_submit():
            set_name = form.set_name.data
            purpose = form.purpose.data

            mycursor.execute(
                'SELECT * FROM sets WHERE set_name = %s', (set_name,))
            existing_set = mycursor.fetchone()

            if existing_set is None:
                # Get last index in Sets Relation
                mycursor.execute(
                    'SELECT * from sets ORDER BY sid DESC LIMIT 1')
                lastRec = mycursor.fetchone()
                if lastRec is None:
                    lastRec = 1
                else:
                    lastRec = lastRec['sid'] + 1

                # Generates Random Code for the Set
                code = uuid.uuid4().hex.upper()[0:10]

                # Insert a New Set for an Organizer
                sql = "INSERT INTO Sets (sid, set_name, purpose, code, organizer) VALUES (%s, %s, %s, %s, %s)"
                val = (lastRec, set_name, purpose, code, session.get('id'))

                mycursor.execute(sql, val)
                mysql.connection.commit()

                # Success Message Appears
                flash('Set Added', 'success')

                # Redirects to Dashboard
                return redirect(url_for('dashboard', username=session.get('username')))
    return render_template('createSet.html', form=form)


@app.route('/<username>/joinSet',  methods=['GET', 'POST'])
def joinASet(username):
    """Render the website's  page."""
    form = joinNewSet()
    if request.method == "POST" and form.validate_on_submit() and session.get('TYPE') == "Regular":
        mycursor = mysql.connection.cursor()
        # Code entered in form for joining a set
        code = form.set_code.data

        # Checks if entered code is valid
        mycursor.execute(
            'SELECT * FROM sets WHERE code = %s', (code,))
        existing_code = mycursor.fetchone()
        # If valid credentials, flash success and redirect
        if existing_code:
            mycursor = mysql.connection.cursor()
            sql = "INSERT INTO joinSet (user_id, sid) VALUES (%s, %s)"
            val = (session.get('id'), existing_code['sid'])
            mycursor.execute(sql, val)
            mysql.connection.commit()

            flash('Successfully Added to Set', 'success')

            return redirect(url_for('dashboard', username=session.get('username')))
    return render_template('joinSet.html', form=form)


@app.route('/members/<sid>',  methods=['GET', 'POST'])
def members(sid):
    mycursor = mysql.connection.cursor()
    mycursor.execute('SELECT * from sets WHERE sid = %s', (sid,))
    fullSet = mycursor.fetchall()

    print(fullSet)

    form = Groupings()

    if 'username' in session and session.get('TYPE') == "Organizer":
        mycursor = mysql.connection.cursor()
        mycursor.execute('SELECT user.first_name, user.last_name from user JOIN regular JOIN joinset ON regular.user_id = user.user_id and regular.user_id = joinset.user_id and user.user_id=joinset.user_id WHERE joinset.sid = %s', (sid,))
        getMembers = mycursor.fetchall()
        print(getMembers)
        print("")
        print("")
        mbrsCopy = getMembers

        if request.method == "POST" and form.validate_on_submit():

            grpBy = form.grpBy.data
            numPersons = form.numPersons.data

            # THIS ONLY ALLOWS FOR THE GROUPS TO SHOW
            length = len(getMembers)
            grpAmt = round(length/int(numPersons))
            mini_gp = []

            for i in range(grpAmt):
                mini_gp = mini_gp + [mbrsCopy[:grpAmt]]
                mbrsCopy = mbrsCopy[grpAmt:]
                # for p in mini_gp[i]:
                #     print("")
                # sug = SetUserGp(user_id=p[1].user_id,
                #                 sid=set_name.sid, gp_num=i+1)
                # db.session.add(sug)
                # db.session.commit()

            # sug = (db.session.query(
            #     SetUserGp).filter_by(sid=set_name.sid).all())

            print("")
            print("")
            # print(sug)
            # print("")
            # print("")
            # lst = []
            # for p in sug:
            #     lst = lst + [p.gp_num]

            # sug = list(dict.fromkeys(lst))
            # sug = getGroups + sug
            # print(sug[-(grpAmt):])

            # return render_template('miniGrps.html', set_name=set_name, numPersons=numPersons, grpAmt=grpAmt, mini_gp=mini_gp, sug=sug)
    return render_template('members.html', sid=sid, form=form, fullSet=fullSet, getMembers=getMembers)


@app.route('/about/<typeUser>', methods=["GET", "POST"])
def aboutUser(typeUser):
    # How am I going to pass the above information
    form = SignUp()
    if request.method == "POST" and form.validate_on_submit():
        user = Regular(type="Regular", first_name=request.form['fname'], last_name=request.form['lname'], email=request.form['email'], username=request.form['username'], password=request.form['password'], gender=request.form['sex'], age=request.form['age'], height=request.form[
            'height'], leadership=request.form['leadership'], ethnicity=request.form['ethnicity'], personality=request.form['personality'], education=request.form['education'], hobby=request.form['hobby'], occupation=request.form['occupation'])

        db.session.add(user)

        # Adds a regular user info to the database
        db.session.commit()

        # Success Message Appears
        flash('You have successfully registered :) ')

        # Redirect User to Main Page
        return redirect(url_for("home"))

        # if form entry is invalid, redirected to the same page to fill in required details
    return render_template('about_you.html', form=form)


@app.route('/Regulars')
def getRegularUsers():
    """Render website's home page."""
    mycursor = mysql.connection.cursor()
    mycursor.execute(
        'SELECT * from user join regular on user.user_id=regular.user_id')
    rv = list(mycursor.fetchall())
    return '<p>' + str(rv) + '</p>'


def randomFeatures():
    # These are random features for the regular user
    gender = random.choice(
        ['Female', 'Male'])
    height = random.randint(142, 198)
    age = random.randint(22, 35)
    leadership = random.choice(
        ['Autocratic', 'Laissez-Faire', 'Democratic'])
    hobby = random.choice(
        ['Sports', 'Music', 'Exercising', 'Shopping', 'Dancing', 'Watching TV', 'Reading and Writing', 'Arts'])
    ethnicity = random.choice(
        ['Black', 'White', 'Chinese', 'Indian', 'Hispanic'])
    occupation = random.choice(
        ['Business', 'Science', 'Technology', 'Construction', 'Communication', 'Law'])
    education = random.choice(
        ['Bachelors', 'Masters', 'PhD', 'Diploma', 'Associate Degree'])
    personality = random.choice(['Introvert', 'Extrovert', 'Ambivert'])

    return [gender, age, height, leadership, ethnicity, personality, education, hobby, occupation]


@app.route('/results',  methods=['GET', 'POST'])
def result():
    """Render the website's result page."""
    return render_template('results.html')


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))
###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

# Flash errors from the form if validation fails


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
