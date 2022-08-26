from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from game_store.models import User, Game

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username Already Exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Already Exists")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateGameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    release_year = StringField('Release Year', validators=[DataRequired()])
    age_rating = StringField('Age Rating', validators=[DataRequired()])
    score = StringField('Score', validators=[DataRequired()])
    developer = StringField('Developer', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()]) 
    update_game = SubmitField('Update')

    def validate_name(self, name):
        # changed_name = name.data
        game = Game.query.filter_by(name=name.data).first()
        if game == game:
            raise ValidationError("Game Already Exists")