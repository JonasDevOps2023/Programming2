from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from datetime import datetime
import pytz


class Database:
    def __init__(self, app):
        self.db = SQLAlchemy(app)

class User(Database.db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)

    def get_swedish_time():
        swedish_tz = pytz.timezone('Europe/Stockholm')
        return datetime.now(swedish_tz)

    registration_date = db.Column(db.DateTime, default=get_swedish_time)
    last_login_date = db.Column(db.DateTime, onupdate=get_swedish_time)