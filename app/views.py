"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import math
import random
from faker import Faker
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, SignUp, Groupings, newSet, joinNewSet
# from app.forms import AboutYou
from werkzeug.security import check_password_hash
from app.models import User, Regular, Administrator, Sets, joinSet, Scores, SetUserGp

fake = Faker()

###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/fakeAdmin/')
def fakesAdministrator():
    for i in range(5):
        typeA = "Administrator"
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        # username = fake.profile(fields=['username'])['username']
        username = first_name
        password = "1234"
        position = fake.profile(fields=['job'])['job']

        adm = Administrator(type=typeA, first_name=first_name, last_name=last_name,
                            email=email, username=username, password=password, position=position)

        db.session.add(adm)
        db.session.commit()

    return render_template('home.html')


@app.route('/fakeRegular/')
def fakesReg():
    for i in range(5):
        typeR = "Regular"
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        gender = fake.profile(fields=['sex'])['sex']
        height = random.randint(142, 198)
        age = random.randint(22, 30)
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
        faculty = random.choice(
            ['Science and Technology', 'Medical Sciences', 'Social Sciences', 'Humanities', 'Engineering', 'Law'])
        # username = fake.profile(fields=['username'])['username']
        username = first_name
        password = "1234"

        adm = Regular(type=typeR, first_name=first_name, last_name=last_name,
                      email=email, username=username, password=password, gender=gender, age=str(age), height=str(height), leadership=leadership, ethnicity=ethnicity, personality=personality, education=education, hobby=hobby, faculty=faculty, occupation=occupation)

        db.session.add(adm)
        db.session.commit()

    return render_template('home.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():

        # Query if User exists
        user = db.session.query(User).filter_by(
            username=form.username.data).first()

        # If valid credentials, flash success and redirect
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login Successful')
            return redirect(url_for('dashboard', username=current_user.username))

        # Flash error message with incorrect username/password
        flash(u'Invalid Credentials', 'error')
    return render_template("login.html", form=form)


@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    """Render the website's dashboard page."""
    if current_user.type == "Administrator":
        getSets = Sets.query.filter_by(
            administrator=current_user.user_id).all()
    else:
        getSets = (
            db.session.query(joinSet, Sets).join(
                joinSet).filter_by(user_id=current_user.user_id).all()
        )
    return render_template('dashbrd.html', gps=getSets)


@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route('/registerAs', methods=["GET", "POST"])
def registerAs():
    """Render the website's register page."""
    if request.method == "POST":
        if request.form.get('Regular') == 'Regular':
            return redirect(url_for('register', typeUser="Regular"))

        elif request.form.get('Administrator') == 'Administrator':
            return redirect(url_for('register', typeUser="Administrator"))
    return render_template('registerAs.html')


@app.route('/register/<typeUser>', methods=["GET", "POST"])
def register(typeUser):
    # First Name, Last Name, Email, Password and Username are collected from the SignUp Form
    form = SignUp()

    if request.method == "POST" and form.validate_on_submit():
        # Collects username and email info from form
        username = form.username.data
        email = form.email.data

        # Checks if another user has this username
        existing_username = db.session.query(
            User).filter_by(username=username).first()

        # Checks if another user has this email address
        existing_email = db.session.query(User).filter_by(email=email).first()

        # If unique email address and username provided then log new user
        if existing_username is None and existing_email is None:
            if typeUser == "Regular":
                user = Regular(type=typeUser, first_name=request.form['fname'], last_name=request.form['lname'],
                               email=request.form['email'], username=request.form['username'], password=request.form['password'], gender="", age="", height="", leadership="", ethnicity="", personality="", education="", hobby="", faculty="", occupation="")
            else:
                user = Administrator(type=typeUser, first_name=request.form['fname'], last_name=request.form['lname'],
                                     email=request.form['email'], username=request.form['username'], password=request.form['password'], position="")
            # Adds a regular user info to the database
            db.session.add(user)
            db.session.commit()

            # Success Message Appears
            flash('Successfully registered', 'success')

            # Logs in a newly registered user
            login_user(user)

            # Redirects to Profile Page
            return redirect(url_for('dashboard', username=user.username))

    # Flash errors in form and redirects to Register Form
    flash_errors(form)
    return render_template("signup.html", form=form)


@login_required
@app.route('/<username>/createSet',  methods=['GET', 'POST'])
def createSet(username):
    """Render the website's  page."""
    form = newSet()
    if request.method == "POST" and form.validate_on_submit():
        set_name = form.set_name.data

        if set_name is not None:
            st = Sets(
                set_name=set_name, purpose=request.form['purpose'], administrator=current_user.user_id)

            # Adds a regular user info to the database
            db.session.add(st)
            db.session.commit()

            # Success Message Appears
            flash('Set Added', 'success')

            # Redirects to Profile Page
            return redirect(url_for('dashboard', username=current_user.username))
    return render_template('createSet.html', form=form)


@login_required
@app.route('/<username>/joinSet',  methods=['GET', 'POST'])
def joinASet(username):
    """Render the website's  page."""
    form = joinNewSet()
    if request.method == "POST" and form.validate_on_submit():
        # Collects username and email info from form
        code = form.set_code.data

        # Checks if another user has this username
        existing_code = db.session.query(
            Sets).filter_by(code=code).first()

        # If valid credentials, flash success and redirect
        if existing_code.code == code:

            join_set = joinSet(user_id=current_user.user_id,
                               sid=existing_code.sid)

            db.session.add(join_set)
            db.session.commit()

            flash('Successfully Added to Set', 'success')

            # return redirect(url_for('dashboard', username=current_user.username))

        return redirect(url_for('dashboard', username=current_user.username))
    return render_template('joinSet.html', form=form)


@login_required
@app.route('/members/<sid>',  methods=['GET', 'POST'])
def members(sid):
    set_name = Sets.query.filter_by(sid=sid).first()
    if current_user.type == "Administrator":
        getMembers = (
            db.session.query(joinSet, Regular, User).join(
                joinSet).filter_by(sid=sid).all()
        )

        mbrsCopy = getMembers

        form = Groupings()
        if request.method == "POST" and form.validate_on_submit():

            grpBy = form.grpBy.data
            numPersons = form.numPersons.data

            # THIS ONLY ALLOWS FOR THE GROUPS TO SHOW
            length = len(getMembers)
            grpAmt = round(length/int(numPersons))
            mini_gp = []

            print("*******")
            print("*******")
            for i in range(grpAmt):
                mini_gp = mini_gp + [mbrsCopy[:grpAmt]]
                mbrsCopy = mbrsCopy[grpAmt:]
                for p in mini_gp[i]:
                    print("")
                    # sug = SetUserGp(user_id=p[1].user_id,
                    #                 sid=set_name.sid, gp_num=i+1)
                    # db.session.add(sug)
                    # db.session.commit()

            getGroups = (db.session.query(
                SetUserGp).filter_by(sid=set_name.sid).all())

            print("")
            print("")
            print(getGroups)

            # return render_template('miniGrps.html', set_name=set_name, numPersons=numPersons, grpAmt=grpAmt, mini_gp=mini_gp)
    return render_template('members.html', getMembers=getMembers, set_name=set_name, sid=sid, form=form)


@app.route('/about/<typeUser>', methods=["GET", "POST"])
def aboutUser(typeUser):
    # How am I going to pass the above information
    form = SignUp()
    if request.method == "POST" and form.validate_on_submit():
        user = Regular(type="Regular", first_name=request.form['fname'], last_name=request.form['lname'], email=request.form['email'], username=request.form['username'], password=request.form['password'], gender=request.form['sex'], age=request.form['age'], height=request.form[
            'height'], leadership=request.form['leadership'], ethnicity=request.form['ethnicity'], personality=request.form['personality'], education=request.form['education'], hobby=request.form['hobby'], faculty=request.form['faculty'], occupation=request.form['occupation'])

        db.session.add(user)

        # Adds a regular user info to the database
        db.session.commit()

        # Success Message Appears
        flash('You have successfully registered :) ')

        # Redirect User to Main Page
        return redirect(url_for("home"))

        # if form entry is invalid, redirected to the same page to fill in required details
    return render_template('about_you.html', form=form)


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
