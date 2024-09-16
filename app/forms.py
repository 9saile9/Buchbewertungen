from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from app.models import User

class LoginForm(FlaskForm):
        username = StringField('Benutzername', validators=[DataRequired()])
        password = PasswordField('Passwort', validators=[DataRequired()])
        remember_me = BooleanField('Benutzer merken')
        submit = SubmitField('Anmelden')

class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField(
        'Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')
    
class EditProfileForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    about_me = TextAreaField('Über mich', validators=[Length(min=0, max=140)])
    submit = SubmitField('speichern')
    
def __init__(self, original_username, *args, **kwargs):
    super(EditProfileForm, self).__init__(*args, **kwargs)
    self.original_username = original_username
    
def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if username.data != self.original_username:
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Bitte einen anderen Benutzernamen verwenden')
        
def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
        raise ValidationError('Bitte eine andere E-Mail-Adresse verwenden')
        
class PostForm(FlaskForm):
    title = StringField('Buchtitel', validators=[DataRequired(), Length(min=1, max=255)])
    general_info = TextAreaField('Allgemeine Informationen', validators=[Length(max=1000)])
    initial_rating = FloatField('Initiale Bewertung', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Buch Posten')

class PostResponseForm(FlaskForm):
    body = TextAreaField('Antwort', validators=[DataRequired()])
    rating = FloatField('Bewertung (optional)', validators=[NumberRange(min=1, max=5)], default=None)
    submit = SubmitField('Antworten')
    
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')