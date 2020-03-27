"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, SignUp
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
    return render_template('dashbrd.html', user=current_user.username)


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
        # Checks in User Table if another user has this username
        username = form.username.data
        email = form.email.data

        existing_username = db.session.query(
            User).filter_by(username=username).first()

        # Checks in User Table if another user has this email address
        existing_email = db.session.query(User).filter_by(email=email).first()
        if existing_username is None and existing_email is None:
            user = User(type=typeUser, first_name=request.form['fname'], last_name=request.form['lname'],
                        email=request.form['email'], username=request.form['username'], password=request.form['password'])

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


@app.route('/about/<typeUser>', methods=["GET", "POST"])
def aboutUser(typeUser):
    # How am I going to pass the above information
    # form = SignUp()
    print(form.username.data)
    if request.method == "POST" and form.validate_on_submit():
        user = Regular(type="regular", first_name=request.form['fname'], last_name=request.form['lname'], email=request.form['email'], username=request.form['username'], password=request.form['password'], gender=request.form['sex'], age=request.form['age'], height=request.form[
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
