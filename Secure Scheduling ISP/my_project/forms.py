#forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired,Email,EqualTo, InputRequired, Length
from wtforms import ValidationError
import pandas as pd

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
    df = pd.read_csv("json_test.csv")
    course_names = df['description']
    course_names.drop_duplicates(inplace=True)
    course_tuple = []
    for i in course_names:
        tmp=i.split('(')
        tmp[0]=tmp[0][:-1]
        tmp2=(tmp[0],tmp[0])
        course_tuple.append(tmp2)

    p1 = SelectField(u'1st Period', choices=course_tuple)
    p2 = SelectField(u'2nd Period', choices=course_tuple)
    p3 = SelectField(u'3rd Period', choices=course_tuple)
    p4 = SelectField(u'4th Period', choices=course_tuple)
    p5 = SelectField(u'5th Period', choices=course_tuple)
    p6 = SelectField(u'6th Period', choices=course_tuple)
    p7 = SelectField(u'7th Period', choices=course_tuple)
    p8 = SelectField(u'8th Period', choices=course_tuple)
    save = SubmitField("Save!")




def check_email(self,field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Your email has been already registered!')

def check_username(self,field):
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Your username has already been registered!')