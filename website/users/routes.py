from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required
from website import bcrypt, db
from website.models import User, Post
from website.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm,\
                                ResetPasswordForm
from website.users.utils import save_picture, send_reset_email

# creating blueprint for users package
users = Blueprint('users', __name__)

# all routes will all assign a header string through Jinja variables to the respective html file so
# it can be used as the header for each page


# will only display if user is not logged in, adds new entry in database for the new user with a hashed
# password if form is valid, will then redirect to login page
@users.route('/register', methods=['post', 'get'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Welcome '+form.username.data+'! Your account has been created. You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", header='Create Your Account', form=form)


# only accessible by not logged in users, will check credetnials to see if they exist in databse before
# logging user in
@users.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', header='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# personal page for each logged in user with their info and a form to modify them (modifies in database
# if form is valid), already fills form fields with users info by querying it form database
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', header='Account', image_file=image_file, form=form)


# generates all posts from database that have the same username as the selected username and orders them
# by date posted, will only display 5 per page
@users.route("/user/<string:username>")
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('Post/user_posts.html', header=username+"'s Posts", posts=posts, user=user)


# can only be accessed by not logged in users, will display form where an email will be enter and checked
# if it exists in the database before sending an email to that email with a link to reset their password
# that link will have a token(random hex string) attached to it with an expiration time
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('password_reset/reset_request.html', header='Reset Password', form=form)


# can only be accessed from an email link with an unique valid token and will display a form where new
# password will be inputted and updated into the database at that user's location
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('password_reset/reset_token.html', header='Reset Password', form=form)