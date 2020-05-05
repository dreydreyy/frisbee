import csv
from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required
from website import db
from website.main.forms import JerseyForm
from website.models import Post, Order

# creating a blueprint for this main package
main = Blueprint('main', __name__)


# all routes will all assign a header string through Jinja variables to the respective html file so
# it can be used as the header for each page


# home page queries first 3 posts from database by time
@main.route('/')
@main.route('/home', methods=['get'])
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=1, per_page=3)
    my_header = "Welcome to Concordia's Ultimate Frisbee Team Official Website!"
    return render_template("Home/home.html", header=my_header, posts=posts)


@main.route('/intro')
def intro():
    my_header = "Introduction"
    return render_template("Intro/intro.html", header=my_header)


# opens a csv file for reading with DictReader which recognizes the first line of the file as the headers
# for each column and the following lines as the values for each column. Used to generate a roster table
@main.route("/team")
def team():
    with open("website/data/roster.csv", 'r') as f:
        csv_reader = csv.DictReader(f)
        my_header = "The Team"
        return render_template("Team/team.html", header=my_header, roster=csv_reader)


@main.route('/how-to-join')
def join():
    my_header = "How to join?"
    return render_template("Join/join.html", header=my_header)


# jersey form that is connected to database table Order, will send valid forms infos to database
@main.route('/jersey', methods=['POST', 'get'])
@login_required
def jersey():
    form = JerseyForm()
    if form.validate_on_submit():
        order = Order(name=form.name.data, number=form.number.data, size=form.size.data, type=form.type.data)
        db.session.add(order)
        db.session.commit()
        flash('Your order has been sent! Contact the moderator for further info', 'success')
        return redirect(url_for('main.jersey'))
    my_header = "Jersey Order"
    return render_template("Info/jersey.html", header=my_header, form=form)


@main.route('/games')
def games():
    my_header = "Pro Ultimate Frisbee Games to Watch"
    return render_template("Info/games.html", header=my_header)


@main.route('/training')
def training():
    my_header = "Training tips"
    return render_template("Info/Training.html", header=my_header)


# opens a csv file for reading with DictReader which recognizes the first line of the file as the headers
# for each column and the following lines as the values for each column. Used to generate a vocabulary list
@main.route('/vocabulary')
def vocab():
    with open("website/data/vocab.csv", 'r') as f:
        csv_reader = csv.DictReader(f)
        my_header = "Some Ultimate Terms"
        return render_template("Info/Ultimate_vocabulary.html", header=my_header, terms=csv_reader)


@main.route('/contact')
def contact():
    my_header = "Contact Information"
    return render_template("Contact/contact.html", header=my_header)
