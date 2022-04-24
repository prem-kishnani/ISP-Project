#app.py
from my_project import app,db
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


@app.route('/home', methods=['GET','POST'])
@login_required
def home(): 
    df = pd.read_csv('schedules.csv',nrows=100000)
    df.set_index('Email',inplace=True)

    form = CourseForm()



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


    return render_template('home.html', form=form)
    
@app.route('/welcome')
@login_required
def welcome_user():
    return redirect(url_for('home'))

@app.route('/logout') 
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/updated')
def updated():
    return render_template("db_updated.html")

if __name__ == '__main__':
    app.run(debug=True)