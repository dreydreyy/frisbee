from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from website.config import Config

# initializing all the variables and programs needed in our application
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


# function that creates our app in a specific configuration, in our case the base one
# we are creating a function to create our app so if we want different version of our application for
# example for testing and for posting online, we can easily create another function and we will just need
# to select which function we want when we run our app
# in this function we are using the configuration variables in our config.py file and introducing all
# initialized variables from before into our app, also we are importing our routes from everyone of our
# packages and registering their blueprints so every part can function harmoniously with the whole
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from website.users.routes import users
    from website.posts.routes import posts
    from website.main.routes import main
    from website.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app