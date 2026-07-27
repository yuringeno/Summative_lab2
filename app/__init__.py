from flask import Flask
from flask_migrate import Migrate

from .models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Ensure routes are registered when importing the app package.
import server  # noqa: F401

