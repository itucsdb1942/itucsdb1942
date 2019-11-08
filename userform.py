from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, Email,EqualTo
class registirationForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname=StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    username=StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    mail =StringField('Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class loginForm(FlaskForm):
    mail =StringField('Mail', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')