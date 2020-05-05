from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from website import db, login_manager
from flask_login import UserMixin


# login tool from flask
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# table which will contain all the users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(30), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # generating a token for resetting the password with an expiration time and passing it the secret
    # key that is unique to our app
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# table which will contain all the jersey orders
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(5), nullable=False)
    type = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Order('{self.name}', '{self.number}', '{self.size}', '{self.type}')"


# table which will contain all the posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
