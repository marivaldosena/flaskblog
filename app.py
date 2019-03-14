import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY') or '3676a9fc1001dca88437094cc3b1610b'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('APP_DATABASE_URL') or 'postgresql://localhost/flaskblog_dev'
db = SQLAlchemy(app)

from models import User, Post

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()[:10]
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@email.com' and \
                        form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
        

    return render_template('login.html', title='Log in', form=form)