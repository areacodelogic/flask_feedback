from flask import Flask, redirect, render_template, jsonify, request, flash, session
from models import User, Feedback, connect_db, db
from forms import AddUserForm, UserLoginForm, FeedbackForm
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
            session["username"] = user.username
            return redirect("/users/<username>")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login_form.html", form=form)


@app.route("/users/<username>")
def display_user_page(username):

    user_from_db = User.query.filter_by(username=username).first()

    all_feedbacks = Feedback.query.all()

    if "username" not in session:
        return redirect("/")

    else: 
        return render_template("user_page.html", user_from_db=user_from_db, feedbacks=all_feedbacks)


@app.route("/logout")
def logout():

    session.pop("username")
    return redirect("/")



@app.route("/users/<username>/feedback/add")
def display_feedback_form(username):

    form = FeedbackForm()
    return render_template("add_feedback_form.html", form=form)


@app.route("/users/<username>/feedback/add", methods=["POST"])
def process_feedback_form(username):

    user_from_db = User.query.filter_by(username=username).first()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = form.username.data
    
        new_feedback = Feedback(title=title, content=content, username=username)
        flash(f"Added {title}")
        
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f"/users/{user_from_db.username}")

    else:
        return render_template("add_feedback_form.html", form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    if session["username"]:

        user_from_db = User.query.filter_by(username=username).first()

        db.session.delete(user_from_db)
        db.session.commit()

    return redirect("/")