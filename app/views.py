"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
import math
# import joblib
# import spacy
# import numpy
# import tensorflow as tf
# import en_core_web_lg
# from operator import itemgetter
# from difflib import SequenceMatcher
from app import app, login_manager
from flask_mysqldb import MySQL
from flask import render_template, request, redirect, url_for, flash, session
from app.forms import LoginForm, SignUp, Groupings, newSet, joinNewSet, AboutYou, Criteria, Profile_About, GroupNum
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

import random
import uuid

# nlp = en_core_web_lg.load()
# nlp = spacy.load('en_core_web_lg')

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

    if 'username' in session and session.get('TYPE') == "Regular":
        mycursor.execute('SELECT user.user_id, username, first_name, last_name, sex, pref_sex, age, height, leadership, education, ethnicity, pref_ethnicity, hobby, occupation, personality from user JOIN regular JOIN joinset ON regular.user_id = user.user_id and regular.user_id = joinset.user_id and user.user_id=joinset.user_id WHERE joinset.sid = %s', (sid,))
        getMembers = list(mycursor.fetchall())
        
        # use score for groups to get actual group members!!
        
        return render_template('miniGrps.html', fullSet=fullSet[0], grpAmt=grpAmt, biography=biography)


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
        flash('Your information has been updated', 'success')

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
    if request.method == "POST" and 'logged_in' in session:
        crit = form.crit.data
        if crit == "compatible":
            mycursor.execute(
                'SELECT * from Scores WHERE `userA username` = %s ORDER BY percentage DESC LIMIT 9', (session['username'],))
        else:
            mycursor.execute(
                'SELECT * from Scores WHERE `userA username` = %s ORDER BY percentage ASC LIMIT 9', (session['username'],))
        matches = list(mycursor.fetchall())
        return render_template('recomnd.html', form=form, matches=matches)
    mycursor.execute(

        'SELECT * from User JOIN Scores ON scores.`userA username`=user.username WHERE scores.`userA username` = %s ORDER BY CSI DESC', (session['username'],))
    matches = list(mycursor.fetchmany(9))
    mycursor.execute(
        'Select * from Biography WHERE user_id = %s', (session['id'],))
    biography = mycursor.fetchone()

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


# personality_wt = 5
# leadership_wt = 5
# hobby_wt = 5

# democratic_meaning = "participative leadership or shared leadership,members of the group take a more participative role in the decision-making process"
# autocratic_meaning = "authoritarian leadership, individual control over all decisions and little input from group members.rarely accept advice from followers"
# laissez_faire_meaning = "delegative leadership,leaders are hands-off and allow group members to make the decisions.lowest productivity among group members"


# ambivert_meaning = "normal overall behavior is between introversion and extroversion"
# extrovert_meaning = "Their outgoing, vibrant nature draws people to them, and they have a hard time turning away the attention. They thrive off the interaction"
# introvert_meaning = "Introverts tend to feel drained after socializing and regain their energy by spending time alone"


# sports_meaning = "activity needing physical effort and skill that is played according to rules, for enjoyment or as a job"
# music_meaning = "an art of sound in time that expresses ideas and emotions in significant forms through the elements of rhythm, melody, harmony, and color"
# exercising_meaning = "activity requiring physical effort, carried out to sustain or improve health and fitness"
# reading_meaning = "cognitive process of decoding symbols to derive meaning"
# shopping_meaning = "Searching for or buying goods"
# writing_meaning = "using symbols to communicate thoughts and ideas in a readable form "
# dancing_meaning = "to move one's body, rhythmically in a pattern of steps"
# arts_meaning = "expression of human creative skill and imagination"
# watching_tv_meaning = "keep under attentive view or observation or view attentively with interest to a broadcast on television"


# # matrix factorization function
# def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.5):
#     Q = Q.T
#     for step in range(steps):
#         for i in range(len(R)):
#             for j in range(len(R[i])):
#                 if R[i][j] > 0:
#                     eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])
#                     for k in range(K):
#                         P[i][k] = P[i][k] + alpha * \
#                             (2 * eij * Q[k][j] - beta * P[i][k])
#                         Q[k][j] = Q[k][j] + alpha * \
#                             (2 * eij * P[i][k] - beta * Q[k][j])
#         eR = numpy.dot(P, Q)
#         e = 0
#         for i in range(len(R)):
#             for j in range(len(R[i])):
#                 if R[i][j] > 0:
#                     e = e + pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
#                     for k in range(K):
#                         e = e + (beta/2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
#         if e < 0.001:
#             break
#     return P, Q.T


# def get_leadership(arg1, arg2, wt):
#     dict_leadership = {"democratic": democratic_meaning,
#                        "autocratic": autocratic_meaning,
#                        "laissez-faire": laissez_faire_meaning}

#     def get_jaccard_sim(str1, str2):
#         a = set(dict_leadership[str1].split())
#         b = set(dict_leadership[str2].split())
#         c = a.intersection(b)
#         d = len(b)+len(a)
#         return float(len(c)) / (d - len(c))

#     def similar(str1, str2):
#         return SequenceMatcher(None, dict_leadership[str1], dict_leadership[str2]).ratio()

# #     def score_same_sim(type1_meaning,type2_meaning): #score_same_sim
# #         meaning1= nlp(dict_leadership[type1_meaning])
# #         remove_stop_words= [str(s) for s in meaning1 if not s.is_stop]
# #         meaning2= nlp(dict_leadership[type2_meaning])
# #         remove_stop_words2= [str(s) for s in meaning2 if not s.is_stop]
# #         meaning1_no_stop_words = nlp(" ".join(remove_stop_words))
# #         meaning2_no_stop_words = nlp(" ".join(remove_stop_words2))
# #         return meaning1_no_stop_words.similarity( meaning2_no_stop_words)

#     def score_same_sim(word, word2):
#         leadership_meaning_lookup_democratic = {
#             'autocratic': 0.83, 'laissez-faire': 0.85269}
#         leadership_meaning_lookup_autocratic = {
#             'democratic': 0.83, 'laissez-faire': 0.80558}
#         leadership_meaning_lookup_laissez_faire = {
#             'autocratic': 0.80558, 'democratic': 0.85269}

#         data_dict = {'democratic': leadership_meaning_lookup_democratic, 'autocratic': leadership_meaning_lookup_autocratic,
#                      'laissez-faire': leadership_meaning_lookup_laissez_faire}
#         word = word.lower()
#         word2 = word2.lower()
#         result = data_dict[word]

#         for i in result:
#             if i == word2:
#                 return float(result[i])

#     def score_same_sim2(word, word2):
#         leadership_sim_lookup_democratic = {
#             'autocratic': 0.5392, 'laissez-faire': 0.2681}
#         leadership_sim_lookup_autocratic = {
#             'democratic': 0.5392, 'laissez-faire': 0.41400838}
#         leadership_sim_lookup_laissez_faire = {
#             'autocratic': 0.41400838, 'democratic': 0.2681}

#         data_dict = {'democratic': leadership_sim_lookup_democratic, 'autocratic': leadership_sim_lookup_autocratic,
#                      'laissez-faire': leadership_sim_lookup_laissez_faire}
#         word = word.lower()
#         word2 = word2.lower()
#         result = data_dict[word]

#         for i in result:
#             if i == word2:
#                 return float(result[i])

#     def leadership_score(type1, type2, wt):
#         return (score_same_sim(type1, type2)+score_same_sim2(type1, type2))/2 + similar(type1, type2) - (wt*get_jaccard_sim(type1, type2))

#     if arg1 == "autocratic" and arg2 == "autocratic":
#         return (leadership_score("autocratic", "laissez-faire", wt) + leadership_score("democratic", "autocratic", wt))/2
#     if arg1 == "laissez-faire" and arg2 == "laissez-faire":
#         return (leadership_score("autocratic", "laissez-faire", wt) + leadership_score("democratic", "laissez-faire", wt))/2
#     if arg1 == "democratic" and arg2 == "democratic":
#         return 1
#     if arg1 == "laissez-faire" or arg2 == "laissez-faire":
#         if arg1 == "laissez-faire":
#             return leadership_score(arg2, arg1, wt)
#         else:
#             return leadership_score(arg1, arg2, wt)
#     else:
#         return leadership_score(arg1, arg2, wt)


# def get_personality(arg1, arg2, wt):

#     dict_psl = {"ambivert": ambivert_meaning,
#                 "extrovert": extrovert_meaning,
#                 "introvert": introvert_meaning}

#     def get_jaccard_sim(str1, str2):
#         a = set(dict_psl[str1].split())
#         b = set(dict_psl[str2].split())
#         c = a.intersection(b)
#         d = len(b)+len(a)
#         return float(len(c)) / (d - len(c))

#     def similar(str1, str2):
#         return SequenceMatcher(None, dict_psl[str1], dict_psl[str2]).ratio()

# #     def score_same_sim(type1_meaning,type2_meaning): #score_same_sim
# #         meaning1= nlp(dict_psl[type1_meaning])
# #         remove_stop_words= [str(s) for s in meaning1 if not s.is_stop]
# #         meaning2= nlp(dict_psl[type2_meaning])
# #         remove_stop_words2= [str(s) for s in meaning2 if not s.is_stop]
# #         meaning1_no_stop_words = nlp(" ".join(remove_stop_words))
# #         meaning2_no_stop_words = nlp(" ".join(remove_stop_words2))
# #         return meaning1_no_stop_words.similarity( meaning2_no_stop_words)
#     def score_same_sim(word, word2):

#         personality_meaning_lookup_ambivert = {
#             'extrovert': 0.46623, 'introvert': 0.589395}
#         personality_meaning_lookpup_extrovert = {
#             'ambivert': 0.46623, 'introvert': 0.78617}
#         personality_meaning_lookpup_introvert = {
#             'ambivert': 0.589395, 'extrovert': 0.78617}

#         data_dict = {'introvert': personality_meaning_lookpup_introvert, 'ambivert': personality_meaning_lookup_ambivert,
#                      'extrovert': personality_meaning_lookpup_extrovert}
#         word = word.lower()
#         word2 = word2.lower()
#         result = data_dict[word]

#         for i in result:
#             if i == word2:
#                 return float(result[i])

#     def score_same_sim2(word, word2):
#         personality_sim_lookup_ambivert = {
#             'extrovert': 0.48455, 'introvert': 0.47561887}
#         personality_sim_lookpup_extrovert = {
#             'ambivert': 0.48455, 'introvert': 0.8067165}
#         personality_sim_lookpup_introvert = {
#             'ambivert': 0.47561887, 'extrovert': 0.8067165}

#         data_dict = {'introvert': personality_sim_lookpup_introvert, 'ambivert': personality_sim_lookup_ambivert,
#                      'extrovert': personality_sim_lookpup_extrovert}
#         word = word.lower()
#         word2 = word2.lower()
#         result = data_dict[word]

#         for i in result:
#             if i == word2:
#                 return float(result[i])

#     def personality_score(type1, type2, wt):
#         return ((score_same_sim(type1, type2)+score_same_sim2(type1, type2))/2)+similar(type1, type2)-(wt*get_jaccard_sim(type1, type2))

#     if arg1 == arg2 and arg1 == "ambivert":
#         return (1 - personality_score("ambivert", "extrovert", wt)) + (1 - personality_score("ambivert", "introvert", wt))
#     if arg1 == arg2 and arg1 == "extrovert":
#         return (1 - personality_score("ambivert", "extrovert", wt)) + (1 - personality_score("extrovert", "introvert", wt))
#     if arg1 == arg2 and arg1 == "introvert":
#         return (1 - personality_score("ambivert", "introvert", wt)) + (1 - personality_score("extrovert", "introvert", wt))
#     if arg1 == "introvert" or arg2 == "introvert":
#         if arg1 == "introvert":
#             return personality_score(arg2, arg1, wt)
#         else:
#             return personality_score(arg1, arg2, wt)
#     if arg1 == "ambivert" or arg2 == "ambivert":
#         if arg1 == "ambivert":
#             return personality_score(arg1, arg2, wt)
#         else:
#             return personality_score(arg2, arg1, wt)


# def get_hobby(arg1, arg2, wt):

#     dict_hobby = {"sports": sports_meaning,
#                   "music": music_meaning,
#                   "exercising": exercising_meaning,
#                   "reading": reading_meaning,
#                   "shopping": shopping_meaning,
#                   "writing": writing_meaning,
#                   "dancing": dancing_meaning,
#                   "arts": arts_meaning,
#                   "watching-tv": watching_tv_meaning
#                   }

#     def get_jaccard_sim(str1, str2):
#         a = set(dict_hobby[str1].split())
#         b = set(dict_hobby[str2].split())
#         c = a.intersection(b)
#         return float(len(c)) / (len(a) + len(b) - len(c))

#     def similar(str1, str2):
#         return SequenceMatcher(None, dict_hobby[str1], dict_hobby[str2]).ratio()

# #     def score_same_sim(type1_meaning,type2_meaning): #score_same_sim
# #         meaning1= nlp(dict_hobby[type1_meaning])
# #         meaning2= nlp(dict_hobby[type2_meaning])
# #         meaning1_no_stop_words = nlp(' '.join([str(t) for t in meaning1 if not t.is_stop]))
# #         meaning2_no_stop_words = nlp(' '.join([str(t) for t in meaning2 if not t.is_stop]))
# #         return meaning1_no_stop_words.similarity( meaning2_no_stop_words)

#     def score_same_sim(word, word2):

#         hobby_meaning_lookup_sports = {'music': 0.77, 'exercising': 0.87, 'reading': 0.613, 'shopping': 0.53,
#                                        'writing': 0.64, 'dancing': 0.61, 'arts': 0.76, 'watching-tv': 0.6016}

#         hobby_meaning_lookup_music = {'sports': 0.77, 'exercising': 0.69, 'reading': 0.647, 'shopping': 0.4467,
#                                       'writing': 0.764, 'dancing': 0.753, 'arts': 0.752, 'watching-tv': 0.57}

#         hobby_meaning_lookup_exercising = {'sports': 0.87, 'music': 0.69, 'reading': 0.59, 'shopping': 0.489,
#                                            'writing': 0.56, 'dancing': 0.61, 'arts': 0.633, 'watching-tv': 0.55}

#         hobby_meaning_lookup_reading = {'sports': 0.613, 'music': 0.647, 'exercising': 0.59, 'shopping': 0.344,
#                                         'writing': 0.74, 'dancing': 0.53, 'arts': 0.612, 'watching-tv': 0.48}

#         hobby_meaning_lookup_shopping = {'sports': 0.53, 'music': 0.4467, 'exercising': 0.489, 'reading': 0.344,
#                                          'writing': 0.41, 'dancing': 0.33, 'arts': 0.35, 'watching-tv': 0.4}

#         hobby_meaning_lookup_writing = {'sports': 0.64, 'music': 0.764, 'exercising': 0.56, 'reading': 0.74,
#                                         'shopping': 0.41, 'dancing': 0.58, 'arts': 0.66, 'watching-tv': 0.582}

#         hobby_meaning_lookup_dancing = {'sports': 0.61, 'music': 0.753, 'exercising': 0.61, 'reading': 0.53,
#                                         'shopping': 0.33, 'writing': 0.58, 'arts': 0.534, 'watching-tv': 0.4132}

#         hobby_meaning_lookup_arts = {'sports': 0.76, 'music': 0.752, 'exercising': 0.633, 'reading': 0.612,
#                                      'shopping': 0.35, 'writing': 0.66, 'dancing': 0.534, 'watching-tv': 0.5}

#         hobby_meaning_lookup_watch_tv = {'sports': 0.6016, 'music': 0.57, 'exercising': 0.55, 'reading': 0.48,
#                                          'shopping': 0.4, 'writing': 0.582, 'dancing': 0.4132, 'arts': 0.5}

#         data_dict = {'watching-tv': hobby_meaning_lookup_watch_tv, 'arts': hobby_meaning_lookup_arts,
#                      'dancing': hobby_meaning_lookup_dancing, 'writing': hobby_meaning_lookup_writing, 'shopping': hobby_meaning_lookup_shopping,
#                      'reading': hobby_meaning_lookup_reading, 'exercising': hobby_meaning_lookup_exercising,
#                      'music': hobby_meaning_lookup_music, 'sports': hobby_meaning_lookup_sports}
#         word = word.lower()
#         word2 = word2.lower()
#         result = data_dict[word]

#         for i in result:
#             if i == word2:
#                 return float(result[i])

#     def score_same_sim2(word, word2):
#         hobby_sim_lookup_sports = {'music': 0.3478885, 'exercising': 0.313734, 'reading': 0.2725, 'shopping': 0.36037,
#                                    'writing': 0.2795706, 'dancing': 0.3233, 'arts': 0.46557, 'watching-tv': 0.4212}

#         hobby_sim_lookup_music = {'sports': 0.3478885, 'exercising': 0.14, 'reading': 0.3018, 'shopping': 0.2290,
#                                   'writing': 0.40106, 'dancing': 0.53523, 'arts': 0.43146, 'watching-tv': 0.40618}

#         hobby_sim_lookup_exercising = {'sports': 0.314, 'music': 0.14, 'reading': 0.29, 'shopping': 0.224,
#                                        'writing': 0.32, 'dancing': 0.33, 'arts': 0.24, 'watching-tv': 0.32588783}

#         hobby_sim_lookup_reading = {'sports': 0.27, 'music': 0.3018, 'exercising': 0.29, 'shopping': 0.2715,
#                                     'writing': 0.7029, 'dancing': 0.25, 'arts': 0.262, 'watching-tv': 0.5}

#         hobby_sim_lookup_shopping = {'sports': 0.36037, 'music': 0.2290, 'exercising': 0.224, 'reading': 0.2715,
#                                      'writing': 0.20046543, 'dancing': 0.26, 'arts': 0.31, 'watching-tv': 0.3049}

#         hobby_sim_lookup_writing = {'sports': 0.2795706, 'music': 0.40106, 'exercising': 0.32, 'reading': 0.7029,
#                                     'shopping': 0.20046543, 'dancing': 0.26433, 'arts': 0.4, 'watching-tv': 0.32}

#         hobby_sim_lookup_dancing = {'sports': 0.3233, 'music': 0.53523, 'exercising': 0.33, 'reading': 0.25,
#                                     'shopping': 0.26, 'writing': 0.26433, 'arts': 0.4, 'watching-tv': 0.5098276}

#         hobby_sim_lookup_arts = {'sports': 0.46557, 'music': 0.43146, 'exercising': 0.24, 'reading': 0.262,
#                                  'shopping': 0.31, 'writing': 0.4, 'dancing': 0.392, 'watching-tv': 0.21286}

#         hobby_sim_lookup_watch_tv = {'sports': 0.4212, 'music': 0.40618, 'exercising': 0.32588783, 'reading': 0.5,
#                                      'shopping': 0.3049, 'writing': 0.32, 'dancing': 0.5098276, 'arts': 0.21286}

#         data_dict = {'watching-tv': hobby_sim_lookup_watch_tv, 'arts': hobby_sim_lookup_arts,
#                      'dancing': hobby_sim_lookup_dancing, 'writing': hobby_sim_lookup_writing, 'shopping': hobby_sim_lookup_shopping,
#                      'reading': hobby_sim_lookup_reading, 'exercising': hobby_sim_lookup_exercising,
#                      'music': hobby_sim_lookup_music, 'sports': hobby_sim_lookup_sports}
#         word = word.lower()
#         word2 = word2.lower()
#         result = data_dict[word]

#         for i in result:
#             if i == word2:
#                 return float(result[i])

#     def hobby_score(type1, type2, wt):
#         return (score_same_sim(type1, type2)+score_same_sim2(type1, type2))/2 + similar(type1, type2) - (wt*get_jaccard_sim(type1, type2))

#     if arg1 == "watching-tv" or arg2 == "watching-tv":
#         if arg1 == "watching-tv":
#             if "reading and writing" in arg2:
#                 return (hobby_score("reading", arg1, wt) + hobby_score("writing", arg1, wt))/2
#             return hobby_score(arg2, arg1, wt)
#         else:
#             if "reading and writing" in arg1:
#                 return (hobby_score("reading", arg2, wt) + hobby_score("writing", arg2, wt))/2
#             return hobby_score(arg1, arg2, wt)
#     if (arg1 == "sports" and arg2 == "exercising") or (arg2 == "sports" and arg1 == "exercising"):
#         return 1
#     if arg1 == arg2:
#         return 1
#     if (arg1 == "dancing" and arg2 == "music") or (arg1 == "dancing" and arg2 == "arts") or \
#         (arg1 == "arts" and arg2 == "music") or (arg2 == "dancing" and arg1 == "music") or \
#             (arg2 == "dancing" and arg1 == "arts") or (arg2 == "arts" and arg1 == "music"):
#         return 1
#     if "reading and writing" in arg1 or "reading and writing" in arg2:
#         if "reading and writing" in arg1:
#             return (hobby_score("reading", arg2, wt) + hobby_score("writing", arg2, wt))/2
#         else:
#             return (hobby_score(arg1, "reading", wt) + hobby_score(arg1, "writing", wt))/2
#     else:
#         return hobby_score(arg1, arg2, wt)


# def age_cal(age, predicted_age, age_recieve):
#     R = numpy.array([[age, predicted_age, 0], [age, age_recieve, 0]])
#     N = len(R)
#     M = len(R[0])
#     K = 2

#     P1 = numpy.array([[0.96618789, 0.28231824],
#                       [0.29011499, 0.05317186]])
#     Q1 = numpy.array([[0.50060064, 0.68964126],
#                       [0.79024825, 0.60951225],
#                       [0.10965169, 0.20230712]])

#     nP, nQ = matrix_factorization(R, P1, Q1, K)
#     nR = numpy.dot(nP, nQ.T)
#     ratio = sum(nR[0]) / sum(nR[1])
#     factorzd = nR[0][2] / nR[1][2]
#     score2 = (factorzd + ratio)/2
#     if predicted_age <= age_recieve:
#         final = (numpy.dot(age, predicted_age) /
#                  numpy.dot(age, age_recieve)) * score2
#         return final
#     else:
#         final = (numpy.dot(age, age_recieve) /
#                  numpy.dot(age, predicted_age)) * score2
#         return final


# def height_cal(height, predicted_ht, ht_recieve):
#     R = numpy.array([[height, predicted_ht, 0], [height, ht_recieve, 0]])
#     N = len(R)
#     M = len(R[0])
#     K = 2
#     P1 = numpy.array([[0.96618789, 0.28231824],
#                       [0.29011499, 0.05317186]])
#     Q1 = numpy.array([[0.50060064, 0.68964126],
#                       [0.79024825, 0.60951225],
#                       [0.10965169, 0.20230712]])

#     nP, nQ = matrix_factorization(R, P1, Q1, K)
#     nR = numpy.dot(nP, nQ.T)
#     ratio = sum(nR[0]) / sum(nR[1])
#     factorzd = nR[0][2] / nR[1][2]
#     score2 = (factorzd + ratio)/2
#     maximum_height = 198
#     minimum_height = 142
#     total_height_levels = maximum_height-minimum_height
#     if predicted_ht <= ht_recieve:
#         level_num = ht_recieve-predicted_ht
#         if level_num > 40:
#             # set maximum height threshold
#             final = (numpy.dot(height, predicted_ht) /
#                      numpy.dot(height, ht_recieve)) * score2
#             return (final * (total_height_levels-(40)))/total_height_levels
#         else:
#             final = (numpy.dot(height, predicted_ht) /
#                      numpy.dot(height, ht_recieve)) * score2
#             return (final * (total_height_levels-(level_num)))/total_height_levels

#     else:
#         final = (numpy.dot(height, predicted_ht) /
#                  numpy.dot(height, ht_recieve)) * score2
#         return (final * (total_height_levels-(predicted_ht-ht_recieve)))/total_height_levels

# # argument 1 gender of the user
# # argument 2 gender preference selected by the user {female,male,either}
# # argument 3 gender of the potential match


# def gender_cal(gender, pref_gender, rec_gender):
#     if gender == "male" or gender == "female":
#         if pref_gender == rec_gender:
#             return 1
#         if pref_gender == "either":
#             return 1
#         else:
#             return 0
#     else:
#         return 0


# def ethnicity_cal(userA_race, userA_ideal_match_race, userB_race):
#     white = {"white": 100, "hispanic": 72,
#              "chinese": 87, "indian": 87, "black": 79}
#     chinese = {"white": 86, "chinese": 100,
#                "hispanic": 69, "indian": 84, "black": 53}
#     black = {"black": 100,  "indian": 70,
#              "chinese": 53, "white": 76, "hispanic": 76}
#     hispanic = {"white": 56, "chinese": 60,
#                 "indian": 60, "black": 50, "hispanic": 100}
#     indian = {"white": 91, "hispanic": 77,
#               "black": 70, "indian": 100, "chinese": 85}
#     ethnicity_list = {"white": white, "chinese": chinese,
#                       "black": black, "hispanic": hispanic, "indian": indian}
#     # print(ethnicity_list)
#     retrieve_ethnicity_dict = ethnicity_list[userA_ideal_match_race]
#     # print(retrieve_ethnicity_dict)
#     for i in retrieve_ethnicity_dict:
#         if i == userB_race:
#             return float(retrieve_ethnicity_dict[i]/100)


# # levels are arrange in ascending order
# # 1- diploma
# # 2- associate degree
# # 3- bachelors
# # 4-masters
# # 5-PHD
# # level = userA current education level
# # predicted-level = AI model prediction about user A best compatible match
# # level_recieve= User B current education level
# def education_cal(level, predicted_level, level_recieve):
#     education_number = {"Diploma": 1, "Associate Degree": 2,
#                         "Bachelors": 3, "Masters": 4, "PhD": 5}
#     R = [
#         [0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0]

#     ]

#     R = numpy.array(R)
#     level = education_number[level]
#     level_recieve = education_number[level_recieve]
#     # print(level,level_recieve)
#     R[0][level-1] = level
#     R[1][level_recieve-1] = level_recieve
#     predicted_level = education_number[predicted_level]
#     N = len(R)
#     M = len(R[0])
#     K = 2

#     P2 = numpy.array([[0.09623613, 0.8288161],
#                       [0.86809128, 0.2776751]])
#     Q2 = numpy.array([[0.21616114, 0.34524425],
#                       [0.19479104, 0.12072784],
#                       [0.26481668, 0.42976937],
#                       [0.57555023, 0.53077791],
#                       [0.34441631, 0.57870231]])

#     nP, nQ = matrix_factorization(R, P2, Q2, K)
#     nR = numpy.dot(nP, nQ.T)
#     if level == level_recieve and predicted_level == level and predicted_level == level_recieve:
#         return 1
#     if level <= level_recieve:
#         user_A = sum(nR[0][:level])
#         user_B = sum(nR[1][:level_recieve])
#         relation = user_A/user_B
#         ratio_rows = sum(nR[0]) / sum(nR[1])
#         level_difference = predicted_level-level
#         if level == level_recieve and level_difference >= 1:
#             # edge cases print("edge case")

#             return predicted_level / (ratio_rows*predicted_level + relation*(int(level_difference)))
#         if predicted_level-level_recieve >= 1 and predicted_level-level >= 1:
#             relation = user_B/user_A
#             return predicted_level / (ratio_rows*predicted_level + relation*(int(level_difference)))
#         else:
#             result = (ratio_rows*predicted_level + relation *
#                       (level_recieve - level)) / level_recieve
#             return result

#     else:
#         user_A = sum(nR[0][:level])
#         user_B = sum(nR[1][:level_recieve])
#         relation = user_B/user_A
#         ratio_rows = sum(nR[1]) / sum(nR[0])
#         if predicted_level-level_recieve >= 1 and predicted_level-level >= 1:
#             relation = user_A/user_B
#             return predicted_level / (ratio_rows*predicted_level + relation*(predicted_level-level_recieve))
#         else:
#             result = (ratio_rows * predicted_level +
#                       relation * (level-level_recieve)) / level
#             return result


# def occupation_cal(curr_occupation, predicted_occupation, rec_occupation):
#     occupation_number = {"Science": 1, "Technology": 2,
#                          "Construction": 3, "Business": 4, "Communication": 5, 'Law': 6}
#     R = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
#     R = numpy.array(R)
#     curr_occupation = occupation_number[curr_occupation]
#     rec_occupation = occupation_number[rec_occupation]
#     R[0][curr_occupation-1] = curr_occupation
#     R[1][rec_occupation-1] = rec_occupation
#     predicted_occupation = occupation_number[predicted_occupation]
#     N = len(R)
#     M = len(R[0])
#     K = 2
#     P1 = numpy.array([[0.63632385, 0.32576404],
#                       [0.28746965, 0.83440233]])
#     Q1 = numpy.array([[0.37123526, 0.74104888],
#                       [0.31432217, 0.65385106],
#                       [0.67300467, 0.40201349],
#                       [0.7737731,  0.36044194],
#                       [0.24890191, 0.40890149],
#                       [0.80346764, 0.2857713]])
#     nP, nQ = matrix_factorization(R, P1, Q1, K)
#     nR = numpy.dot(nP, nQ.T)
#     if curr_occupation == rec_occupation and predicted_occupation == curr_occupation and predicted_occupation == rec_occupation:
#         return 1
#     if predicted_occupation == rec_occupation:
#         return 1
#     if curr_occupation <= rec_occupation:
#         user_A = sum(nR[0][:curr_occupation])
#         user_B = sum(nR[1][:rec_occupation])
#         relation = user_A/user_B
#         ratio_rows = sum(nR[0]) / sum(nR[1])
#         occ_diff = predicted_occupation-curr_occupation
#         if curr_occupation == rec_occupation and occ_diff >= 1:
#             # edge cases print("edge case")
#             return predicted_occupation / (ratio_rows*predicted_occupation + relation*(int(occ_diff)))
#         if predicted_occupation-rec_occupation >= 1 and predicted_occupation-curr_occupation >= 1:

#             relation = user_B/user_A
#             return predicted_occupation / (ratio_rows*predicted_occupation + relation*(int(occ_diff)))
#         else:
#             result = (ratio_rows*predicted_occupation + relation *
#                       (rec_occupation - curr_occupation)) / rec_occupation
#             return result

#     else:
#         user_A = sum(nR[0][:curr_occupation])
#         user_B = sum(nR[1][:rec_occupation])
#         relation = user_B/user_A
#         ratio_rows = sum(nR[1]) / sum(nR[0])
#         occ_diff = predicted_occupation-rec_occupation
#         if predicted_occupation-rec_occupation >= 1 and predicted_occupation-curr_occupation >= 1:

#             return predicted_occupation / (ratio_rows*predicted_occupation + relation*(int(occ_diff)))
#         else:
#             result = (ratio_rows * predicted_occupation + relation *
#                       (curr_occupation-rec_occupation))/curr_occupation
#             return result


# # dt={"gender":'Male', 'height':'170', 'leadership':'autocratic', 'ethnicity':'black', 'personality':}
# def convert_user_matrix_userA(lst):
#     lst = lst[0]

#     personality_number = {"Introvert": 0, "Ambivert": 1, "Extrovert": 2}
#     leadership_number = {"Laissez-Faire": 0, "Democratic": 1, "Autocratic": 2}
#     hobby_number = {"Sports": 0, "Music": 1, "Exercising": 2, "Shopping": 3,
#                     "Dancing": 4, "Watching-TV": 5, "Reading and Writing": 6, "Arts": 7}
#     gender_number = {'Female': 0, 'Male': 1}
#     ethnicity_number = {"Black": 0, "White": 1,
#                         "Chinese": 2, "Indian": 3, "Hispanic": 4}
#     education_number = {"Diploma": 0, "Associate Degree": 1,
#                         "Bachelors": 2, "Masters": 3, "PhD": 4}
#     occupation_number = {"Science": 0, "Technology": 1,
#                          "Construction": 2, "Business": 3, "Communication": 4, 'Law': 5}
#     return [[personality_number[lst['personality']], leadership_number[lst['leadership']], hobby_number[lst['hobby']]],
#             [gender_number[lst['sex']], int(lst['age']), int(lst['height'])],
#             [ethnicity_number[lst['ethnicity']], education_number[lst['education']], occupation_number[lst['occupation']]]]


# def convert_user_matrix(lst):

#     personality_number = {"Introvert": 0, "Ambivert": 1, "Extrovert": 2}
#     leadership_number = {"Laissez-Faire": 0, "Democratic": 1, "Autocratic": 2}
#     hobby_number = {"Sports": 0, "Music": 1, "Exercising": 2, "Shopping": 3,
#                     "Dancing": 4, "Watching-TV": 5, "Reading and Writing": 6, "Arts": 7}
#     gender_number = {'Female': 0, 'Male': 1}
#     ethnicity_number = {"Black": 0, "White": 1,
#                         "Chinese": 2, "Indian": 3, "Hispanic": 4}
#     education_number = {"Diploma": 0, "Associate Degree": 1,
#                         "Bachelors": 2, "Masters": 3, "PhD": 4}
#     occupation_number = {"Science": 0, "Technology": 1,
#                          "Construction": 2, "Business": 3, "Communication": 4, 'Law': 5}
#     return [[personality_number[lst['personality']], leadership_number[lst['leadership']], hobby_number[lst['hobby']]],
#             [gender_number[lst['sex']], int(lst['age']), int(lst['height'])],
#             [ethnicity_number[lst['ethnicity']], education_number[lst['education']], occupation_number[lst['occupation']]]]


# def unconvert_user_matrix(lst):

#     personality_number = {0: "Introvert", 1: "Ambivert", 2: "Extrovert"}
#     leadership_number = {0: "Laissez-Faire", 1: "Democratic", 2: "Autocratic"}
#     hobby_number = {0: "Sports", 1: "Music", 2: "Exercising", 3: "Shopping",
#                     4: "Dancing", 5: "Watching-TV", 6: "Reading and Writing", 7: "Arts"}
#     gender_number = {0: 'Female', 1: 'Male'}
#     ethnicity_number = {0: "Black", 1: "White",
#                         2: "Chinese", 3: "Indian", 4: "Hispanic"}
#     education_number = {0: "Diploma", 1: "Associate Degree",
#                         2: "Bachelors", 3: "Masters", 4: "PhD"}
#     occupation_number = {0: "Science", 1: "Technology",
#                          2: "Construction", 3: "Business", 4: "Communication", 5: 'Law'}
#     return [[personality_number[lst[0][0]], leadership_number[lst[0][1]], hobby_number[lst[0][2]]],
#             [gender_number[lst[1][0]], lst[1][1], lst[1][2]],
#             [ethnicity_number[lst[2][0]], education_number[lst[2][1]], occupation_number[lst[2][2]]]]

# #print(unconvert_user_matrix([[0, 1, 6], [1, 22, 180], [1, 3, 1]]))


# loaded_model_age = joblib.load('finalized_model_age.sav')
# loaded_model_height = joblib.load('finalized_model_height.sav')
# personality_model = tf.keras.models.load_model('personality_model')
# leadership_model = tf.keras.models.load_model('leadership_model')
# hobby_model = tf.keras.models.load_model('hobby_model')
# education_model = tf.keras.models.load_model('education_model_5_features')
# occupation_model = tf.keras.models.load_model('occupation_model_5_features')

# #newlist= sorted(result, key=itemgetter('CSI'))


# def REGCSI(userA, db):
#     list_of_persons = []
#     print('>>>>>>>>>', userA)
#     #predicted_userA= unconvert_user_matrix(model(convert_user_matrix(userA)))
#     details_userA = userA[0]
#     numeric_userA = convert_user_matrix_userA(userA)
#     print('>>>>>>', numeric_userA)
#     #numeric_userB= userB
#     words_userA = unconvert_user_matrix(numeric_userA)
#     # print('userA:',userA)
#     #userB= unconvert_user_matrix(userB)
#     # print('userB:',userB)
#     # name=details_userA['username']
#     # print('name',name)
#     age_pred = int(loaded_model_age.predict(
#         [[numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]]))
#     height_pred = int(loaded_model_height.predict(
#         [[numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]]))

#     personality_pred = numpy.argmax(personality_model.predict(numpy.array(
#         [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
#     leadership_pred = numpy.argmax(leadership_model.predict(numpy.array(
#         [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
#     hobby_pred = numpy.argmax(hobby_model.predict(numpy.array(
#         [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[0][2], numeric_userA[1][0], numeric_userA[1][1], numeric_userA[1][2]]])))
#     education_pred = numpy.argmax(education_model.predict(numpy.array(
#         [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[1][0], numeric_userA[2][1], numeric_userA[2][2]]])))
#     occupation_pred = numpy.argmax(occupation_model.predict(numpy.array(
#         [[numeric_userA[0][0], numeric_userA[0][1], numeric_userA[1][0], numeric_userA[2][1], numeric_userA[2][2]]])))

#     predicted_user_matrix = [[personality_pred, leadership_pred, hobby_pred], [
#         numeric_userA[1][0], age_pred, height_pred], [numeric_userA[2][0], education_pred, occupation_pred]]
#     #print("predicted user matrix: ",predicted_user_matrix)
#     con_predicted_user_matrix = unconvert_user_matrix(predicted_user_matrix)
#     #print('occupation:  ',occupation_pred)
#     #print("predicted user matrix:    ",con_predicted_user_matrix)
#     for i in db:
#         # print("loop",i)
#         userB = convert_user_matrix(i)
#         userB = unconvert_user_matrix(userB)
#         personality_csi = get_personality(
#             con_predicted_user_matrix[0][0].lower(), i['personality'].lower(), personality_wt)

#         leadership_csi = get_leadership(
#             con_predicted_user_matrix[0][1].lower(), i['leadership'].lower(), leadership_wt)

#         hobby_csi = get_hobby(
#             con_predicted_user_matrix[0][2].lower(), i['hobby'].lower(), hobby_wt)
#         gender_csi = gender_cal(words_userA[1][0].lower(
#         ), details_userA['pref_sex'].lower(), i['sex'].lower())
#         age_csi = age_cal(
#             int(words_userA[1][1]), con_predicted_user_matrix[1][1], int(i['age']))
#         height_csi = height_cal(
#             int(words_userA[1][2]), con_predicted_user_matrix[1][2], int(i['height']))
#         ethnicity_csi = ethnicity_cal(words_userA[2][0].lower(
#         ), details_userA['pref_ethnicity'].lower(), i['ethnicity'].lower())
#         education_csi = education_cal(
#             words_userA[2][1], con_predicted_user_matrix[2][1], i['education'])
#         occupation_csi = occupation_cal(
#             words_userA[2][2], con_predicted_user_matrix[2][2], i['occupation'])
#         #print('occupation csi:',occupation_csi,words_userA[2][2],con_predicted_user_matrix[2][2],i['occupation'] )
#         # name2=i['username']
#         # print('name2',name2)

#         total = personality_csi+leadership_csi + hobby_csi + gender_csi + \
#             age_csi + height_csi + ethnicity_csi + education_csi + occupation_csi
#         results = {"userA username ": details_userA['username'], "userB username": i['username'], 'CSI': total,


#                    'personality_score': round(float(personality_csi), 3), 'leadership_score': round(float(leadership_csi), 3),
#                    'hobby_score': round(float(hobby_csi), 3), 'gender_score': int(gender_csi), 'age_score': round(float(age_csi), 3), 'height_score': round(float(height_csi), 3),
#                    'ethnicity_score': round(float(ethnicity_csi), 3),  'education_score': round(float(education_csi), 3), 'occupation_score': round(float(occupation_csi), 3),


#                    'con_personality_score': int((personality_csi/total)*100), 'con_leadership_score': int((leadership_csi/total)*100),
#                    'con_hobby_score': int((hobby_csi/total)*100), 'con_gender_score': int((gender_csi/total)*100), 'con_age_score': int((age_csi/total)*100), 'con_height_score': int((height_csi/total)*100),
#                    'con_ethnicity_score': int((ethnicity_csi/total)*100),  'con_education_score': int((education_csi/total)*100), 'con_occupation_score': int((occupation_csi/total)*100)}

#         list_of_persons.append(results)
#         #print("results   :        ",results)
#     top_nine = sorted(list_of_persons, key=itemgetter('CSI'), reverse=True)
#     top_nine = top_nine[0:9]
#     bottom_nine = sorted(list_of_persons, key=itemgetter('CSI'))
#     bottom_nine = bottom_nine[0:9]
#     print("top 9:          ", top_nine)
#     print("bottom 9:          ", bottom_nine)
#     return list_of_persons, bottom_nine, top_nine

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
