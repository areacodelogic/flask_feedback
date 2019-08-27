from flask import Flask, redirect, render_template, jsonify, request, flash, session
from models import User, connect_db, db
from forms import AddUserForm, UserLoginForm
import bcrypt
from flask_bcrypt import Bcrypt
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def home():

    return redirect("/register")


@app.route("/register")
def display_register_form():

    form = AddUserForm()
    return render_template("add_user_form.html", form=form)


@app.route("/register", methods=["POST"])
def process_register_form():

    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
    
        new_user = User.register(username, password, email, first_name, last_name)
        flash(f"Added {username}")
        
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    else:
        return render_template("add_user_form.html", form=form)


@app.route("/login")
def display_login_form():

    form = UserLoginForm()

    return render_template("login_form.html", form=form)


@app.route("/login", methods=["POST"])
def login():
    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        flash(f"Hi {username} !")
        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.id
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login_form.html", form=form)


@app.route("/secret")
def display_secret_page():

    return render_template("secret_page.html")