from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])

    password_confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=6)])

    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()

        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()

        if user:
            raise ValidationError('E-mail is already taken.')


class LoginForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
