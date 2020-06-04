"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
import math


from app import app, login_manager
from flask_mysqldb import MySQL
from flask import render_template, request, redirect, url_for, flash, session
from app.forms import LoginForm, SignUp, Groupings, newSet, joinNewSet, AboutYou, Criteria, Profile_About, GroupNum
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

import random
import uuid


###
# Routing for your application.
###

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'csi'
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


@app.route('/testimonies/')
def testimonies():
    """Render the website's about page."""
    return render_template('testimonies.html')


@app.route('/admin/', methods=["GET", "POST"])
def admin():
    """Render the website's admin page."""
    form = adminSettings()

    mycursor = mysql.connection.cursor()
    mycursor.execute('Select * from Dictionary')
    definitions = mycursor.fetchone()

    if request.method == "POST" and form.validate_on_submit():
        pers_weight = request.form['pers_weight']
        ldrshp_weight = request.form['ldrshp_weight']
        hobby_weight = request.form['hobby_weight']
        democratic = request.form['democratic']
        autocratic = request.form['autocratic']
        laissezfaire = request.form['laissezfaire']
        ambivert = request.form['ambivert']
        extrovert = request.form['extrovert']
        introvert = request.form['introvert']
        sports = request.form['sports']
        music = request.form['music']
        exercising = request.form['exercising']
        reading = request.form['reading']
        shopping = request.form['shopping']
        writing = request.form['writing']
        dancing = request.form['dancing']
        arts = request.form['arts']
        watchingTV = request.form['watchingTV']

        mycursor = mysql.connection.cursor()

        if pers_weight:
            sql = "UPDATE Dictionary SET personality_weight = %s  WHERE dict_id = %s"
            val = (pers_weight, 'D-01')
            mycursor.execute(sql, val)
            mysql.connection.commit()

        if ldrshp_weight:
            sql = "UPDATE Dictionary SET leadership_weight = %s WHERE dict_id = %s"
            val = (ldrshp_weight, 'D-01')
            mycursor.execute(sql, val)
            mysql.connection.commit()

        if hobby_weight:
            sql = "UPDATE Dictionary SET hobby_weight = %s WHERE dict_id = %s"
            val = (hobby_weight, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if democratic:
            sql = "UPDATE Dictionary SET democratic = %s WHERE dict_id = %s"
            val = (democratic, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if autocratic:
            sql = "UPDATE Dictionary SET autocratic = %s WHERE dict_id = %s"
            val = (autocratic, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if laissezfaire:
            sql = "UPDATE Dictionary SET laissez_faire = %s WHERE dict_id = %s"
            val = (laissezfaire, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if ambivert:
            sql = "UPDATE Dictionary SET ambivert = %s WHERE dict_id = %s"
            val = (ambivert, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if extrovert:
            sql = "UPDATE Dictionary SET extrovert = %s WHERE dict_id = %s"
            val = (extrovert, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if introvert:
            sql = "UPDATE Dictionary SET introvert = %s WHERE dict_id = %s"
            val = (introvert, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if sports:
            sql = "UPDATE Dictionary SET sports = %s WHERE dict_id = %s"
            val = (sports, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if music:
            sql = "UPDATE Dictionary SET music = %s WHERE dict_id = %s"
            val = (music, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if exercising:
            sql = "UPDATE Dictionary SET exercising = %s WHERE dict_id = %s"
            val = (exercising, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if reading:
            sql = "UPDATE Dictionary SET reading = %s WHERE dict_id = %s"
            val = (reading, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if shopping:
            sql = "UPDATE Dictionary SET shopping = %s WHERE dict_id = %s"
            val = (shopping, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if writing:
            sql = "UPDATE Dictionary SET writing = %s WHERE dict_id = %s"
            val = (writing, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if dancing:
            sql = "UPDATE Dictionary SET dancing = %s WHERE dict_id = %s"
            val = (dancing, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if arts:
            sql = "UPDATE Dictionary SET arts = %s WHERE dict_id = %s"
            val = (arts, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        if watchingTV:
            sql = "UPDATE Dictionary SET watching_tv = %s WHERE dict_id = %s"
            val = (watchingTV, 'D-01')

            mycursor.execute(sql, val)
            mysql.connection.commit()

        flash('Settings Updated', 'success')

    return render_template('admin.html', form=form, definitions=definitions)


@app.route('/admin/currentusers/', methods=["GET", "POST"])
def allUsers():
    mycursor = mysql.connection.cursor()
    mycursor.execute('Select * from user WHERE user_id != %s',
                     (session['id'],))
    users = mycursor.fetchall()

    return render_template('all_users.html', users=users)


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

        # If existing user
        if user:
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['id'] = user['user_id']
            session['username'] = request.form['username']
            session['TYPE'] = user['type']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']

            if user['type'] == 'Administrator':
                return redirect(url_for('admin'))

            else:
                flash('Login Successful', 'success')
                return redirect(url_for('dashboard', username=username))

        # Flash error message with incorrect username/password
        flash('Invalid Credentials', 'danger')
    return render_template("login.html", form=form)


@app.route('/dashboard/<username>', methods=["GET", "POST"])
def dashboard(username):
    """Render the website's dashboard page."""
    if 'username' in session:
        mycursor = mysql.connection.cursor()
        mycursor.execute('Select * from user WHERE username = %s', (username,))
        user = mycursor.fetchone()

        if session.get('TYPE') == "Organizer":
            mycursor.execute(
                'SELECT * FROM sets WHERE organizer = %s ', (session['id'],))
        else:
            mycursor.execute(
                'SELECT * FROM Sets JOIN joinset ON sets.sid = joinset.sid WHERE joinset.user_id = %s ', (session['id'],))

        getSets = mycursor.fetchall()

        if session.get('TYPE') == "Regular":
            mycursor.execute(
                'SELECT * FROM user JOIN pin_user ON user.user_id = pin_user.match_id WHERE pin_user.user_id = %s ', (session['id'],))
            getFriends = mycursor.fetchall()

        mycursor.execute(
            'Select * from Biography WHERE user_id = %s', (session['id'],))
        biography = mycursor.fetchone()

    return render_template('dashbrd.html', groups=getSets, type=session.get('TYPE'), biography=biography)


@app.route("/edit/<username>", methods=["GET", "POST"])
def edit_info(username):
    PropicForm = Profile_About()
    mycursor = mysql.connection.cursor()

    mycursor.execute(
        'Select * from Biography WHERE user_id = %s', (session['id'],))
    biography = mycursor.fetchone()

    if request.method == "POST" and PropicForm.validate_on_submit():
        profPic = request.files['profPic']
        about = PropicForm.about.data

        filename = secure_filename(profPic.filename)

        if filename != "":  # INCASE THEY RE-EDIT AND DONT UPLOAD A PHOTO
            profPic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if biography != None:
            if filename != "" and about != "":  # IF PERSON UPDATES BOTH
                sql = "UPDATE Biography SET pro_photo = %s, about = %s WHERE user_id = %s"
                val = (filename, about, session['id'])
            elif filename != "":  # IF PERSON UPDATES PHOTO ONLY
                sql = "UPDATE Biography SET pro_photo = %s WHERE user_id = %s"
                val = (filename, session['id'])
            else:  # IF PERSON UPDATES ABOUT ONLY
                sql = "UPDATE Biography SET about = %s WHERE user_id = %s"
                val = (about, session['id'])

            mycursor.execute(sql, val)
            mysql.connection.commit()

        else:  # EDIT FOR THE FIRST TIME
            sql = "INSERT INTO Biography (user_id, pro_photo, about) VALUES (%s, %s, %s)"
            val = (session['id'], filename, about)
            mycursor.execute(sql, val)
            mysql.connection.commit()

        flash('Your edits were saved', 'success')
        redirect(url_for('dashboard',  username=session.get('username')))

    return render_template('edit.html', PropicForm=PropicForm, biography=biography)


@app.route("/logout")
def logout():
    # Logout the user and end the session
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('type', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
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

                sql = "INSERT INTO Regular (user_id, sex, age, height, leadership, ethnicity, personality, education, hobby, occupation, pref_sex, pref_ethnicity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (mycursor.lastrowid, randFt[0], randFt[1],
                       randFt[2], randFt[3], randFt[4], randFt[5], randFt[6], randFt[7], randFt[8], randFt[9], randFt[10])

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

    form = Groupings()
    mycursor.execute(
        'Select * from Biography WHERE user_id = %s', (session['id'],))
    biography = mycursor.fetchone()
    if 'username' in session and session.get('TYPE') == "Organizer":
        mycursor.execute('SELECT user.user_id, username, first_name, last_name, sex, pref_sex, age, height, leadership, education, ethnicity, pref_ethnicity, hobby, occupation, personality from user JOIN regular JOIN joinset ON regular.user_id = user.user_id and regular.user_id = joinset.user_id and user.user_id=joinset.user_id WHERE joinset.sid = %s', (sid,))
        getMembers = list(mycursor.fetchall())

        if request.method == "POST" and form.validate_on_submit() and int(form.numPersons.data) <= len(getMembers):
            criteria = form.grpBy.data    # Compatible or Incompatible
            # Number of Persons in Each Group
            numPersons = int(form.numPersons.data)

            # Total Amount of Persons in Set
            length = len(getMembers)
            # How many Groups Formed
            grpAmt = round(len(getMembers)/numPersons)

            # mycursor.execute(
            #     'DELETE from SetUserGroup WHERE sid = %s', (sid,))

            # mycursor.execute(
            #     'DELETE from SetGroupScore WHERE sid = %s', (sid,))

            # # # CSI MAGIC

            # for i in range(grpAmt):
            #     sql = "INSERT INTO SetUserGroup (username, sid, group_num) VALUES (%s, %s, %s)"
            #     val = (results[i][0]['userA username '], sid, i+1)

            #     mycursor.execute(sql, val)
            #     mysql.connection.commit()
            #     for result in results[i]:
            #         sql = "INSERT INTO SetUserGroup (username, sid, group_num) VALUES (%s, %s, %s)"
            #         val = (result['userB username'], sid, i+1)

            #         mycursor.execute(sql, val)
            #         mysql.connection.commit()

            #         sql = "INSERT INTO SetGroupScore (`userA username`, `userB username`, sid, group_num, CSI, percentage, personality_score, leadership_score, hobby_score, gender_score, age_score, height_score, ethnicity_score, education_score, occupation_score, con_personality_score, con_leadership_score, con_hobby_score, con_gender_score, con_age_score, con_height_score, con_ethnicity_score, con_education_score, con_occupation_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            #         val = (result['userA username '], result['userB username'], sid, i+1, result['CSI'],  result['Percentage'], result['personality_score'], result['leadership_score'], result['hobby_score'], result['gender_score'], result['age_score'], result['height_score'], result['ethnicity_score'], result['education_score'],
            #                result['occupation_score'], result['con_personality_score'], result['con_leadership_score'], result['con_hobby_score'], result['con_gender_score'], result['con_age_score'], result['con_height_score'], result['con_ethnicity_score'], result['con_education_score'], result['con_occupation_score'])

            #         mycursor.execute(sql, val)
            #         mysql.connection.commit()

            return render_template('miniGrps.html', fullSet=fullSet[0], numPersons=numPersons, grpAmt=grpAmt, biography=biography)
    return render_template('members.html', sid=sid, form=form, fullSet=fullSet, getMembers=getMembers, biography=biography)


@app.route('/Group/<sid>', methods=["GET", "POST"])
def groupMembers(sid):
    numb = GroupNum()

    mycursor = mysql.connection.cursor()
    mycursor.execute('SELECT * from sets WHERE sid = %s', (sid,))
    fullSet = mycursor.fetchall()

    mycursor.execute(
        'Select * from Biography WHERE user_id = %s', (session['id'],))
    biography = mycursor.fetchone()

    if request.method == "POST" and numb.validate_on_submit():
        group_num = int(numb.group_num.data)

        mycursor.execute(
            'SELECT first_name, last_name, user.username from User JOIN SetUserGroup on SetUserGroup.username = user.username WHERE group_num = %s ', (group_num, ))
        mems = mycursor.fetchall()

        mycursor.execute(
            'SELECT sum(CSI) as CSI, sum(percentage) as percentage, sum(personality_score) as personality_score, sum(leadership_score) as leadership_score, sum(hobby_score) as hobby_score, sum(gender_score) as gender_score, sum(age_score) as age_score, sum(height_score) as height_score, sum(ethnicity_score) as ethnicity_score, sum(education_score) as education_score, sum(occupation_score) as occupation_score, count(CSI) as amount from SetUserGroup JOIN SetGroupScore ON SetGroupScore.`userA username` = SetUserGroup.username AND SetGroupScore.group_num = SetUserGroup.group_num WHERE SetUserGroup.sid = %s AND SetGroupScore.group_num = %s', (sid, group_num, ))
        cur_set = mycursor.fetchall()

        print(cur_set[0])

        return render_template('groupMembers.html', group_num=group_num, mems=mems, cur_set=cur_set[0], fullSet=fullSet[0], numb=numb, biography=biography)
    return render_template('groupMembers.html', fullSet=fullSet[0], numb=numb, biography=biography)


@app.route('/about/<typeUser>', methods=["GET", "POST"])
def aboutUser(typeUser):
    form = AboutYou()
    mycursor = mysql.connection.cursor()

    if request.method == "POST" and form.validate_on_submit():

        sql = """UPDATE Regular SET sex = %s, age = %s, height = %s, leadership = %s, ethnicity = %s, personality = %s, education = %s, hobby = %s, occupation = %s, pref_sex = %s, pref_ethnicity = %s WHERE user_id = %s"""
        val = (request.form['sex'], request.form['age'],
               request.form['height'], request.form['leadership'], request.form['ethnicity'], request.form['personality'], request.form['education'], request.form['hobby'], request.form['occupation'], request.form['pref_sex'], request.form['pref_ethnicity'], session.get('id'))
        mycursor.execute(sql, val)
        mysql.connection.commit()

        # Success Message Appears
        flash('Your information has been updated :) ', 'success')

        # Redirect User to Main Page
        return redirect(url_for("dashboard", username=session.get('username')))

        # if form entry is invalid, redirected to the same page to fill in required details

    mycursor.execute(
        'Select * from Biography WHERE user_id = %s', (session['id'],))
    biography = mycursor.fetchone()

    return render_template('about_you.html', form=form, biography=biography)


@app.route('/recommend/<username>', methods=['GET', 'POST'])
def recommend(username):
    """Render the website's recommended matches page."""
    form = Criteria()

    mycursor = mysql.connection.cursor()
    mycursor.execute(
        'Select * from Biography WHERE user_id = %s', (session['id'],))
    biography = mycursor.fetchone()

    if request.method == "POST" and 'logged_in' in session:
        crit = form.crit.data
        if crit == "compatible":
            mycursor.execute(
                'SELECT * from Scores WHERE `userA username` = %s ORDER BY percentage DESC LIMIT 9', (session['username'],))
        else:
            mycursor.execute(
                'SELECT * from Scores WHERE `userA username` = %s ORDER BY percentage ASC LIMIT 9', (session['username'],))
        matches = list(mycursor.fetchall())
        return render_template('recomnd.html', form=form, matches=matches, biography=biography)
    mycursor.execute(

        'SELECT * from User JOIN Scores ON scores.`userA username`=user.username WHERE scores.`userA username` = %s ORDER BY CSI DESC', (session['username'],))
    matches = list(mycursor.fetchmany(9))

    return render_template('recomnd.html', form=form, matches=matches, biography=biography)


@app.route('/run')
def run():
    # CSI Magic
    # comp_list is the variable for the list returned by CSI
    # how many persons are we submitting to the database 25 ???
    mycursor = mysql.connection.cursor()
    mycursor.execute(
        'DELETE from Scores WHERE `userA username` = %s', (session['username'],))

    # Index 0 has in the 25 or so people to write to the db
    for user in comp_list[0]:
        # insert response to database
        sql = "INSERT INTO Scores (`userA username`, `userB username`, CSI, percentage, personality_score, leadership_score, hobby_score, gender_score, age_score, height_score, ethnicity_score, education_score, occupation_score, con_personality_score, con_leadership_score, con_hobby_score, con_gender_score, con_age_score, con_height_score, con_ethnicity_score, con_education_score, con_occupation_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # userA username has an extra space
        val = (user['userA username '], user['userB username'], user['CSI'], int((user['CSI'] / 9) * 100), user['personality_score'], user['leadership_score'], user['hobby_score'], user['gender_score'], user['age_score'], user['height_score'], user['ethnicity_score'], user['education_score'],
               user['occupation_score'], user['con_personality_score'], user['con_leadership_score'], user['con_hobby_score'], user['con_gender_score'], user['con_age_score'], user['con_height_score'], user['con_ethnicity_score'], user['con_education_score'], user['con_occupation_score'])

        mycursor.execute(sql, val)
        mysql.connection.commit()
    return redirect(url_for('recommend', username=session.get('username')))


@app.route('/users')
def getUsers():
    """Render website's home page."""
    mycursor = mysql.connection.cursor()

    mycursor.execute(
        'SELECT username, first_name, last_name, sex, pref_sex, age, height, leadership, education, ethnicity, pref_ethnicity, hobby, occupation, personality from user join regular on user.user_id=regular.user_id WHERE user.username = %s', (session['username'],))
    userA = list(mycursor.fetchall())    # Current User

    mycursor.execute(
        'SELECT username, first_name, last_name, sex, pref_sex, age, height, leadership, education, ethnicity, pref_ethnicity, hobby, occupation, personality from user join regular on user.user_id=regular.user_id WHERE NOT user.username = %s', (session['username'],))
    other_users = list(mycursor.fetchall())     # All but current user

    return '<p>' + str(cur_user) + '</p>' + '<p>' + str(other_users) + '</p>'


def randomFeatures():
    # These are random features for the regular user
    sex = random.choice(
        ['Female', 'Male'])
    pref_sex = random.choice(
        ['Female', 'Male'])
    height = random.randint(142, 198)
    age = random.randint(22, 35)
    leadership = random.choice(
        ['Autocratic', 'Laissez-Faire', 'Democratic'])
    hobby = random.choice(
        ['Sports', 'Music', 'Exercising', 'Shopping', 'Dancing', 'Watching-TV', 'Reading', 'Writing', 'Arts'])
    ethnicity = random.choice(
        ['Black', 'White', 'Chinese', 'Indian', 'Hispanic'])
    pref_ethnicity = random.choice(
        ['Black', 'White', 'Chinese', 'Indian', 'Hispanic'])
    occupation = random.choice(
        ['Business', 'Science', 'Technology', 'Construction', 'Communication', 'Law'])
    education = random.choice(
        ['Bachelors', 'Masters', 'PhD', 'Diploma', 'Associate Degree'])
    personality = random.choice(['Introvert', 'Extrovert', 'Ambivert'])

    return [sex, age, height, leadership, ethnicity, personality, education, hobby, occupation, pref_sex, pref_ethnicity]


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
