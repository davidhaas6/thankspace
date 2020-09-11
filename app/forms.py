from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from config import Config
from app import db
from app.models import User


class GratefulForm(FlaskForm):
    item1 = StringField('Number 1', validators=[DataRequired(), Length(max=Config.MAX_ITEM_LEN, message=f"Each entry must be {Config.MAX_ITEM_LEN} characters or less")])
    item2 = StringField('Number 2', validators=[DataRequired(), Length(max=Config.MAX_ITEM_LEN, message=f"Each entry must be {Config.MAX_ITEM_LEN} characters or less")])
    item3 = StringField('Number 3', validators=[DataRequired(), Length(max=Config.MAX_ITEM_LEN, message=f"Each entry must be {Config.MAX_ITEM_LEN} characters or less")])
    submit = SubmitField('Share')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address incorrect format")])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Email address incorrect format"), 
            Length(max=Config.MAX_EMAIL_LEN, message=f"Email address must be {Config.MAX_EMAIL_LEN} characters or less")
    ])

    handle = StringField('Handle', validators=[DataRequired(), 
            Regexp(Config.HANDLE_REGEX, message="Handle may only contain alphanumeric characters and underscore"),
            Length(max=Config.MAX_HANDLE_LEN, message=f"Handle must be {Config.MAX_HANDLE_LEN} characters or less"),
    ])

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])

    submit = SubmitField('Register')


# For following and unfollowing
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
