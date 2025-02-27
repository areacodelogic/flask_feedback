from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, TextAreaField 

class AddUserForm(FlaskForm):
    """form for adding users"""

    username = StringField("Username")
    password = StringField("Password")
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")


class UserLoginForm(FlaskForm):

    username = StringField("Username")
    password = StringField("Password")


class FeedbackForm(FlaskForm):

    title = StringField("Title")
    content = TextAreaField("Content")
    username = StringField("Username")




