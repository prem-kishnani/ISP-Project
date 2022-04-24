#forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo, InputRequired, Length
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField('Register!')

class CourseForm(FlaskForm):
    p1 = TextAreaField("1st Period",validators=[DataRequired(),Length(max=30)])
    p2 = TextAreaField("2nd Period",validators=[DataRequired(),Length(max=30)])
    p3 = TextAreaField("3rd Period",validators=[DataRequired(),Length(max=30)])
    p4 = TextAreaField("4th Period",validators=[DataRequired(),Length(max=30)])
    p5 = TextAreaField("5th Period",validators=[DataRequired(),Length(max=30)])
    p6 = TextAreaField("6th Period",validators=[DataRequired(),Length(max=30)])
    p7 = TextAreaField("7th Period",validators=[DataRequired(),Length(max=30)])
    p8 = TextAreaField("8th Period",validators=[DataRequired(),Length(max=30)])
    save = SubmitField("Save!")

def check_email(self,field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Your email has been already registered!')

def check_username(self,field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Your username has already been registered!')