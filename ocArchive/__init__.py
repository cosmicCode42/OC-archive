import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"):
    import env

from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri


db = SQLAlchemy(app)


from ocArchive import routes


# Create an instance of the LoginManager class
login_manager = LoginManager()
login_manager.init_app(app)  # Initialize Flask-Login with Flask app


from ocArchive.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure the login manager
login_manager.login_view = 'login'