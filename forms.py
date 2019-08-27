from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, TextAreaField 

class AddUserForm(FlaskForm):
    """form for adding users"""

    username = StringField("Username")
    password = StringField("Password")
    email = StringField("Email")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")




