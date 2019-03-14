import os
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY') or '3676a9fc1001dca88437094cc3b1610b'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('APP_DATABASE_URL') or 'postgresql://localhost/flaskblog_dev'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def __str__(self):
        return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def __str__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


@app.route('/')
@app.route('/home')
def home():
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

if __name__ == '__main__':
    app.run()