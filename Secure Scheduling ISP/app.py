#app.py
from my_project import app,db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from my_project.models import User
from my_project.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np

df = pd.read_csv('schedules.csv')
df_transposed = df.transpose()

@app.route('/')
def home():
    return render_template('home.html', tables=[df_transposed[[1]].to_html(classes='data')],titles=df.columns.values)
    
@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout') 
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))


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
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)