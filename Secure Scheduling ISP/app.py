#app.py imports, from __init__.py (my project) and from Python libraries(flask_login, time, pandas, numpy, etc.,)
from my_project import app,db,auth, serve
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from my_project.models import User
from my_project.forms import LoginForm, RegistrationForm, CourseForm
from werkzeug.security import generate_password_hash, check_password_hash
from my_project.email_func import email_verification
import pandas as pd
import numpy as np
import time
import smtplib, ssl
import json


# This takes you to the API Documentation page
@app.route('/api-doc')
def apidoc():
    return render_template("api_doc.html")

#This was designed to be a test function and see whether or not the message shown would work. There is no LOGIN_REQUIRED message here
@app.route('/rest-unauth')
def open_response():
    dictionary=dict()
    dictionary["Ok"]="Anyone can see this message without authentication"
    return dictionary

#Login_required here, and this is to check for authentication.
@app.route('/rest-auth')
@auth.login_required
def get_response():
    dictionary = dict()
    dictionary["Success!"]="You are authorized to see this message"
    return dictionary

#Get method
@app.route('/api/get', methods=['GET'])
@auth.login_required
def get_schedule():
    # Asks for an email (?email=)
    args = request.args
    email = args.get("email")
    #Email inputted incorrectly, handle error
    if email is None:
        dictionary = dict()
        dictionary["Incorrect Request"]=f"Your request was not correct. A proper endpoint would be {URL}/api/get?email= with you inputting your email at the end."
        return dictionary
    
    df = pd.read_csv('schedules.csv',nrows=100000)
    df.set_index('Email',inplace=True)
    dictionary = dict()
    dictionary["Email"]=f"{email}"
    
    try:
        for i in range(1,9):
            dictionary[f"Period {i}"]=df.at[email,f"Period {i}"]
    except:
        dictionary = dict()
        dictionary["KeyError"]=f"{email} is not in database. Try again with a valid email" 

    #Either will return an error or the right one.
    return dictionary

# User without a blank user
@app.route('/api/post/blankuser',methods=['POST'])
@auth.login_required
def add_user():
    #Get the json body inputted by the user.
    some_json=request.get_json()
    try:
        key_email = some_json["email"]
    except:
        #No email field inputted. 
        dictionary=dict()
        dictionary["KeyError"] = "You did not input an 'email' field."
        return dictionary
    df = pd.read_csv('schedules.csv',nrows=100000)
    df.set_index('Email',inplace=True)
    #Result is ok, because the email is not in the database and all params are correct.
    if key_email not in df.index:
        df.at[key_email] = None
        df.to_csv("schedules.csv")
        dictionary = dict()
        dictionary["Email"]=key_email
        dictionary["Result"]="Ok"
        return dictionary
    # Email is already in the database, which is an error. Can't have duplicate emails.
    else:
        dictionary=dict()
        dictionary["Error"]="Your email is already in the database."
        return dictionary

# User with schedule requires proper params (email, p1, p2, p3, p4, p5, p6, p7, p8)
@app.route('/api/post/userwschedule',methods=['POST'])
@auth.login_required
def add_schedule():
    # Get the JSON body
    some_json=request.get_json()
    # If the email is there, get the information
    try:
        key_email = some_json["email"]
    # If not, then we need to return the error.
    except:
        dictionary=dict()
        dictionary["KeyError"] = "You did not input an 'email' field."
        return dictionary
    # Key_classes is an empty list that we can store classes in.
    key_classes = []
    # If all the params are correct, put it in
    try:
        for i in range(1,9):
            key_classes.append(some_json[f"p{i}"])
    # Error message for not having all the proper parameters.
    except:
        dictionary=dict()
        dictionary["Error"]="Please use all the right parameters for your input. REFERENCE"
        return dictionary

    # Read the courses from the json csv file, remove the duplicates (no need for 1st-2nd semester, and then sort values alphabetically)
    df = pd.read_csv("json_test.csv")
    course_names = df['description']
    course_names.drop_duplicates(inplace=True)
    course_names = course_names.sort_values(ascending=True)
    # Remove excess stuff from the string, then append the course_name to a list.
    course_names_list = []
    for i in course_names:
        tmp=i.split('(')
        tmp=tmp[0][:-1]
        course_names_list.append(tmp)

    # Error message if the key_class is not available (ex: someone inputs something silly like AP Minecraft, Advanced Fortnite, poop, etc.,)
    for key_class in key_classes:
        if key_class not in course_names_list:
            dictionary=dict()
            dictionary["Error"]=f"{key_class} is not in the list of available classes."
            return dictionary
    # Read the csv of schedules and make sure that the email is unique. 
    df = pd.read_csv('schedules.csv',nrows=100000)
    df.set_index('Email',inplace=True)
    if key_email not in df.index:
        df.at[key_email] = None
        for i in range(1,9):
            df.at[key_email,f"Period {i}"]=key_classes[i-1]
        df.to_csv("schedules.csv")
        dictionary = dict()
        dictionary["Email"]=key_email
        dictionary["Result"]="Ok"
        return dictionary
    # If not, handle the error
    else :
        dictionary=dict()
        dictionary["Error"]="Your email is already in the database."
        return dictionary

# Get and Post are methods, but it is for the FlaskForm, no API call here (default homepage)
@app.route('/home', methods=['GET','POST'])
@login_required
def home(): 
    df = pd.read_csv('schedules.csv',nrows=100000)
    df.set_index('Email',inplace=True)

    
    form = CourseForm()

    # Validate on Submit checks for whether the user has inputted a login and password
    if form.validate_on_submit():
        print('Validated Form')
        print(form.p1.data)
        print(current_user.email)
        #1. Read values and store them in our dataframe
        df.at[current_user.email,"Period 1"] = form.p1.data
        df.at[current_user.email,"Period 2"] = form.p2.data
        df.at[current_user.email,"Period 3"] = form.p3.data
        df.at[current_user.email,"Period 4"] = form.p4.data
        df.at[current_user.email,"Period 5"] = form.p5.data
        df.at[current_user.email,"Period 6"] = form.p6.data
        df.at[current_user.email,"Period 7"] = form.p7.data
        df.at[current_user.email,"Period 8"] = form.p8.data
        print(df.loc[current_user.email])

        #2. Overwrite the csv file
        df.to_csv("schedules.csv") 

        return redirect(url_for('updated'))

    if current_user.is_authenticated:

        # If email not in DF index then add a row with that user and blank values for Periods in DF
        if current_user.email not in df.index:
            df.at[current_user.email] = None

        # Some print statements here for error checking. Each item is the dropdown. 
        schedule = []
        print(current_user.email)
        for i in range(1,9):
            class_name = df.loc[current_user.email,f"Period {i}"]
            schedule.append(class_name)
        form.p1.data = schedule[0]
        form.p2.data = schedule[1]
        form.p3.data = schedule[2]
        form.p4.data = schedule[3]
        form.p5.data = schedule[4]
        form.p6.data = schedule[5]
        form.p7.data = schedule[6]
        form.p8.data = schedule[7]

    # Render_template is the default method of Flask to return a webpage, with any necessary params.
    return render_template('home.html', form=form)

# Welcome is a default page.
@app.route('/welcome')
@login_required
def welcome_user():
    return redirect(url_for('home'))

# Logout page just flashes the message and logs out the user: uses flask_login method (pre-built)
@app.route('/logout') 
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Login: if validated, it will login successfully, else it will stay un logged
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Logged in Succesfully!")

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('welcome_user')
            
            return redirect(next)

    return render_template('login.html', form=form) 

#Register a new user manually without API
@app.route('/register',methods=['GET','POST'])
def register(): 
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Thanks for registration!")
        #EMAIL FUNCTION HERE
        email_verification(user.email)

        time.sleep(3)
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

#When db is updated it will show this page
@app.route('/updated')
def updated():
    return render_template("db_updated.html")

if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0",port="8080",ssl_context="adhoc")  -> Non-waitress serve, waitress works better
    serve(app,host="0.0.0.0",port="8080",url_scheme="https")