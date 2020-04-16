"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import math
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, SignUp, Groupings, newGroup, joinNewGroup
# from app.forms import AboutYou
from werkzeug.security import check_password_hash
from app.models import User, Regular, Organizer, Grouped, joinGroup, Scores


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
    if current_user.type == "Organizer":
        getGroups = Grouped.query.filter_by(
            administrator=current_user.user_id).all()
    else:
        getGroups = (
            db.session.query(joinGroup, Grouped).join(
                joinGroup).filter_by(user_id=current_user.user_id).all()
        )
    return render_template('dashbrd.html', gps=getGroups)


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

        elif request.form.get('Organizer') == 'Organizer':
            return redirect(url_for('register', typeUser="Organizer"))
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
                               email=request.form['email'], username=request.form['username'], password=request.form['password'], gender="", age="", height="", leadership="", ethnicity="", personality="", education="", hobby="", faculty="", work="")
            else:
                user = Organizer(type=typeUser, first_name=request.form['fname'], last_name=request.form['lname'],
                                 email=request.form['email'], username=request.form['username'], password=request.form['password'], occupation="")
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
@app.route('/<username>/createGroup',  methods=['GET', 'POST'])
def createGroup(username):
    """Render the website's  page."""
    form = newGroup()
    if request.method == "POST" and form.validate_on_submit():
        gp_name = form.group_name.data

        if gp_name is not None:
            gp = Grouped(
                group_name=gp_name, purpose=request.form['purpose'], administrator=current_user.user_id)

            # Adds a regular user info to the database
            db.session.add(gp)
            db.session.commit()

            # Success Message Appears
            flash('Group Added', 'success')

            # Redirects to Profile Page
            return redirect(url_for('dashboard', username=current_user.username))
    return render_template('createGroup.html', form=form)


@login_required
@app.route('/<username>/joinGroup',  methods=['GET', 'POST'])
def joinAGroup(username):
    """Render the website's  page."""
    form = joinNewGroup()
    if request.method == "POST" and form.validate_on_submit():
        # Collects username and email info from form
        code = form.group_code.data

        # Checks if another user has this username
        existing_code = db.session.query(
            Grouped).filter_by(code=code).first()

        # If valid credentials, flash success and redirect
        if existing_code.code == code:

            join_gp = joinGroup(user_id=current_user.user_id,
                                group_id=existing_code.group_id)

            db.session.add(join_gp)
            db.session.commit()

            flash('Successfully Added to Group')

            # return redirect(url_for('dashboard', username=current_user.username))

        return redirect(url_for('dashboard', username=current_user.username))
    return render_template('joinGroup.html', form=form)


@login_required
@app.route('/members/<gp_id>',  methods=['GET', 'POST'])
def members(gp_id):
    gp_name = Grouped.query.filter_by(group_id=gp_id).first()
    if current_user.type == "Organizer":
        getMembers = (
            db.session.query(joinGroup, Regular, User).join(
                joinGroup).filter_by(group_id=gp_id).all()
        )

        mbrsCopy = getMembers

        form = Groupings()
        if request.method == "POST" and form.validate_on_submit():

            grpBy = form.grpBy.data
            numPersons = form.numPersons.data

            # THIS ONLY ALLOWS FOR THE GROUPS TO SHOW

            length = len(getMembers)
            print("Length: ", length)

            grpAmt = round(length/int(numPersons))
            print("grpAmt rounded: ", grpAmt)

            gp = []
            for i in getMembers:
                gp = gp + [i[1].first_name + " " + i[1].last_name]

            return redirect(url_for('miniGrps', gp_id=gp_id, grpAmt=grpAmt, numPersons=numPersons))

    return render_template('members.html', getMembers=getMembers, gp_name=gp_name, gp_id=gp_id, form=form)


@login_required
@app.route('/minigroups/<gp_id>/<numPersons>/<grpAmt>',  methods=['GET', 'POST'])
def miniGrps(gp_id, numPersons, grpAmt):
    gp_name = Grouped.query.filter_by(group_id=gp_id).first()
    return render_template('miniGrps.html', gp_name=gp_name, numPersons=numPersons, grpAmt=int(grpAmt))


@app.route('/about/<typeUser>', methods=["GET", "POST"])
def aboutUser(typeUser):
    # How am I going to pass the above information
    form = SignUp()
    if request.method == "POST" and form.validate_on_submit():
        user = Regular(type="Regular", first_name=request.form['fname'], last_name=request.form['lname'], email=request.form['email'], username=request.form['username'], password=request.form['password'], gender=request.form['sex'], age=request.form['age'], height=request.form[
            'height'], leadership=request.form['leadership'], ethnicity=request.form['ethnicity'], personality=request.form['personality'], education=request.form['education'], hobby=request.form['hobby'], faculty=request.form['faculty'], work=request.form['work'])

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
