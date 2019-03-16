import os
import secrets
from PIL import Image
from flask import Flask, render_template, flash, \
    redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, \
    login_user, current_user, logout_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv(
    'APP_SECRET_KEY') or '3676a9fc1001dca88437094cc3b1610b'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'APP_DATABASE_URL') or 'postgresql://localhost/flaskblog_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from models import User, Post
from forms import RegistrationForm, LoginForm, UpdateAccountForm, \
    PostForm

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account created for {form.username.data}! You can login now.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash('You have been logged in!', 'success')

            if next_page:
                return redirect(request.host + next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check e-mail and password.', 'danger')

    return render_template('login.html', title='Log in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if  form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    else:
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account Info',
        image_file=image_file, form=form)


@app.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
            author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('posts/new.html',
        title='New Post', form=form)


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html',
        title=post.title, post=post)

@app.route('/posts/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('show_post', post_id=post.id))
        
    form.title.data = post.title
    form.content.data = post.content

    return render_template('posts/new.html',
        title='Update Post', post=post, form=form)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pics', picture_fn)

    output_size = (128, 128)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
