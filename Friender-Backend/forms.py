from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class CSRFDisabledForm(FlaskForm):
    """CSRF disabled form"""
    class Meta:
        csrf = False


class LoginForm(CSRFDisabledForm):
    """Login Form
      csrf disabled
    """

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(CSRFDisabledForm):
    """Register Form
      csrf disabled
    """

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
