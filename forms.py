from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,RadioField,DateField,BooleanField, DecimalField
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError
from userdb import username_check, mail_check
from books import check_tpage

class registirationForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname=StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    username=StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    mail =StringField('Mail', validators=[DataRequired(), Email()])
    gender=RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    date=DateField('Date of Birth', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = username_check(username.data)
        if user: 
            raise ValidationError('That username is taken!')

    def validate_mail(self, mail):
        user = mail_check(mail.data)
        if user: 
            raise ValidationError('That e-mail is taken!')

class loginForm(FlaskForm):
    username =StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class tvForm(FlaskForm):
    title= StringField('Title',validators=[DataRequired()])
    language= StringField('Language',validators=[DataRequired()])
    year= DecimalField('Year',validators=[DataRequired()])
    season= DecimalField('Season',validators=[DataRequired()])
    genre= StringField('Genre',validators=[DataRequired()])
    channel= StringField('Channel',validators=[DataRequired()])
    submit = SubmitField('Add Tv Series')
    
class bookForm(FlaskForm):
    name= StringField('Title',validators=[DataRequired()])
    writer = StringField('Author',validators=[DataRequired()])
    year_pub = DecimalField('Year of Publication',validators=[DataRequired()])
    tpage = DecimalField('Total Page',validators=[DataRequired()])
    publisher = StringField('Publisher',validators=[DataRequired()])
    language = StringField('Language',validators=[DataRequired()])
    genre = StringField('Genre',validators=[DataRequired()])
    submit = SubmitField('Add Book')
 
class UpdateForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    mail =StringField('Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
            user = username_check(username.data)
            if user: 
                raise ValidationError('That username is taken!')

    def validate_mail(self, mail):
            user = mail_check(mail.data)
            if user: 
                raise ValidationError('That e-mail is taken!')

