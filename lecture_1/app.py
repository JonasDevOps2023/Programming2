from flask import Flask, request, url_for, render_template, redirect, make_response
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

from forms import RegisterForm, LoginForm

from datetime import datetime

from markupsafe import escape

import secrets




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Hirviturkki:123456@localhost/lecture_1_website'
db = SQLAlchemy(app)

app.static_folder = 'static'

hidden_key = secrets.token_urlsafe(32)
app.secret_key = hidden_key

""" target="_blank"  """

# Bootstrap-Flask
bootstrap = Bootstrap5(app)
# Flask-WTF
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(120), default="default_profile_pic.jpg")
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return self.is_approved

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)




@app.route("/")
def index():
    resp = make_response(render_template('index.html'))
    return render_template('index.html')


@app.route("/hello_world")
def hello():
    resp = make_response(render_template('hello_world.html'))
    return resp

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    message = None

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        full_name = form.full_name.data
        is_approved = False
        
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            message = "Username is already taken. Please choose a different username."
        elif existing_email:
            message = "Email is already in use. Please use another email."
        else:
            user = User(username=username, email=email, full_name=full_name, is_approved=is_approved)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            message = f"Account created successfully! It will be approved shortly. {user.is_approved}"
    return render_template('create_account.html', form=form, message=message)

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_authenticated():
        name = current_user.full_name
        username = current_user.username
        return render_template('dashboard.html', name=name, username=username)
    return redirect('login')

@app.route("/me")
def me_api():
    return {
        "username": "Hirviturkki",
        "name": "Jonas",
        "lastname": "Pajari",
        "age": 30
    }


#@app.route("/upload")
#def upload_file():


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = None

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password_hash, form.password.data):
            if user.is_authenticated():
            #if is_approved
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                message = "You're not approved. You have to wait.."
                return render_template('login.html', form=form, message=message)
        message = f"Invalid username of password, user: {bool(user)} password: {check_password_hash(user.password_hash, form.password.data)}"
        return render_template('login.html', form=form, message=message)

    return render_template('login.html', form=form, message=message)
