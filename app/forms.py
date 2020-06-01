from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    "Form used to log in an existing User - Regular / Organizer"

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')


class SignUp(FlaskForm):
    "Form used to Register a New User"
    fname = StringField('First Name:', validators=[DataRequired(), Length(
        min=4, max=30, message=('Name should be Characters Only'))])

    lname = StringField('Last Name:', validators=[DataRequired(), Length(
        min=4, max=30, message=('Name should be Characters Only'))])

    email = StringField('Email Address', validators=[
                        DataRequired(), Email(message=('Please enter a valid email address.'))])

    username = StringField('Username', validators=[DataRequired(), Length(
        min=4, max=30, message=('Username should not exceed 30 characters'))])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
    ])

    confirmPassword = PasswordField('Repeat Password', [
        EqualTo('password', message='Passwords must match.')
    ])

    submit = SubmitField('Next')


class AboutYou(FlaskForm):
    sex = SelectField(
        'Sex', choices=[(0, 'Select an option'), ('Female', 'Female'), ('Male', 'Male')])

    pref_sex = SelectField('Your preferred sex:', choices=[(
        0, 'Select an option'), ('Female', 'Female'), ('Male', 'Male')])

    age = StringField('Age', validators=[DataRequired()])

    height = SelectField('Height', choices=[(0, 'Select an option'), ('142', '(4 ft 8 inches) 142 cm'), (
        '144', '(4 ft 9 inches) 144 cm'), ('147', '(4 ft 10 inches) 147 cm'), ('149', '(4 ft 11 inches)  149 cm'), ('152', '(5 ft 0 inches)	152 cm'), ('154', '(5 ft 1 inches)	154 cm'), ('157', '(5 ft 2 inches)	157 cm'), ('160', '(5 ft 3 inches)	160 cm'), ('162', '(5 ft 4 inches)	162 cm'), ('165', '(5 ft 5 inches)	165 cm'), ('168', '(5 ft 6 inches)	168 cm'), ('170', '(5 ft 7 inches)	170 cm'), ('172', '(5 ft 8 inches)	172 cm'), ('175', '(5 ft 9 inches)	175 cm'), ('177', '(5 ft 10 inches)	177 cm'), ('180', '(5 ft 11 inches) 180 cm'), ('183', '(6 ft 0 inches)	183 cm'), ('185', '(6 ft 1 inches)	185 cm'), ('188', '(6 ft 2 inches)	188 cm'), ('191', '(6 ft 3 inches)	191 cm'), ('194', '(6 ft 4 inches)	194 cm'), ('196', '(6 ft 5 inches)	196 cm'), ('198', '(6 ft 6 inches)	198 cm')])

    ethnicity = SelectField('What is your ethnicity?', choices=[(0, 'Select an option'), (
        'Black', 'Black (Coloured)'), ('Chinese', 'Chinese'), ('White', 'White'), ('Indian', 'Indian'), ('Hispanic', 'Hispanic')])

    pref_ethnicity = SelectField('Your preferred ethnicity:', choices=[(0, 'Select an option'), (
        'Black', 'Black (Coloured)'), ('Chinese', 'Chinese'), ('White', 'White'), ('Indian', 'Indian'), ('Hispanic', 'Hispanic')])

    personality = SelectField('What is your personality type?', choices=[(0, 'Select an option'), (
        'Introvert', 'Introvert'), ('Extrovert', 'Extrovert'), ('Ambivert', 'Ambivert')])

    occupation = SelectField('To which work area do you belong?', choices=[(0, 'Select an option'), ('Business', 'Business'), ('Education', 'Education'), (
        'Science', 'Science'), ('Technology', 'Technology'), ('Construction', 'Construction'), ('Communication', 'Communication'), ('Law', 'Law')])

    leadership = SelectField('Which is your leadership style?', choices=[(0, 'Select an option'), (
        'Democratic', 'Democratic'), ('Autocratic', 'Autocratic'), ('Laissez-Faire', 'Laissez-Faire')])

    education = SelectField('Which is your level of education?', choices=[(0, 'Select an option'), ('Bachelors', 'Bachelors'), (
        'Masters', 'Masters'), ('PhD', 'PhD'), ('Diploma', 'Diploma'), ('Associate Degree', 'Associate Degree')])

    hobby = SelectField('What is your favourite hobby?', choices=[(0, 'Select an option'), ('Sports', 'Sports'), (
        'Music', 'Music'), ('Exercising', 'Exercising'), ('Shopping', 'Shopping'), ('Dancing', 'Dancing'), ('Watching-TV', 'Watching TV'), ('Reading', 'Reading'), ('Writing', 'Writing'), ('Arts', 'Arts')])

    submit = SubmitField('Submit')


class newSet(FlaskForm):
    set_name = StringField('Set Name:', validators=[DataRequired(), Length(
        min=4, max=30, message=('Name should be Characters Only'))])

    purpose = StringField('Purpose:', validators=[DataRequired(), Length(
        min=4, max=30, message=('Name should be Characters Only'))])

    submit = SubmitField('Add New Set')


class joinNewSet(FlaskForm):
    set_code = StringField('Code:', validators=[DataRequired(), Length(
        min=4, max=30, message=('Name should be Characters Only'))])

    submit = SubmitField('Join Set')


class Groupings(FlaskForm):
    grpBy = SelectField('Criteria', choices=[(
        0, 'Select an option'), ('compatible', 'Compatible'), ('uncompatible', 'Uncompatible')])

    numPersons = IntegerField('Number of Persons: ',
                             validators=[DataRequired()])

    submit = SubmitField('Create')


class GroupNum(FlaskForm):
    group_num = StringField('Group Number: ', validators=[DataRequired()])

    submit = SubmitField('Get')


def intcheck(self, field):
    try:
        val = int(field.data)
    except ValueError:
        raise ValidationError('Must be a number')


class TranferGrp(FlaskForm):
    # NOT WOKRING :(
    grpNum = IntegerField('First Group Number', validators=[
                          DataRequired(), intcheck])
    grpNum2 = IntegerField('Second Group Number', validators=[
                           DataRequired(), intcheck])

    submit = SubmitField('Next')


class Criteria(FlaskForm):
    crit = SelectField('Criteria', choices=[
                       ('compatible', 'Compatible'), ('incompatible', 'Incompatible')])


class adminSettings(FlaskForm):
    pers_weight = SelectField('Personality', choices=[
                              ('5', '5'), ('10', '10')])
    ldrshp_weight = SelectField('Leadership', choices=[
                                ('5', '5'), ('10', '10')])
    hobby_weight = SelectField('Hobby', choices=[('5', '5'), ('10', '10')])
    democratic = TextAreaField('Democratic', validators=[Length(max=500)])
    autocratic = TextAreaField('Autocratic', validators=[Length(max=500)])
    laissezfaire = TextAreaField('Laissez-Faire', validators=[Length(max=500)])
    ambivert = TextAreaField('Ambivert', validators=[Length(max=500)])
    extrovert = TextAreaField('Extrovert', validators=[Length(max=500)])
    introvert = TextAreaField('Introvert', validators=[Length(max=500)])
    sports = TextAreaField('Sports', validators=[Length(max=500)])
    music = TextAreaField('Music', validators=[Length(max=500)])
    exercising = TextAreaField('Exercising', validators=[Length(max=500)])
    reading = TextAreaField('Reading', validators=[Length(max=500)])
    shopping = TextAreaField('Shopping', validators=[Length(max=500)])
    writing = TextAreaField('Writing', validators=[Length(max=500)])
    dancing = TextAreaField('Dancing', validators=[Length(max=500)])
    arts = TextAreaField('Arts', validators=[Length(max=500)])
    watchingTV = TextAreaField('Watching TV', validators=[Length(max=500)])
    submit = SubmitField('Save')
