from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')], render_kw={"placeholder": "Retype Password"})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username or Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone Number', render_kw={"placeholder": "Phone Number"})
    message = CKEditorField('Message', validators=[DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField('Submit')


class DateForm(FlaskForm):
    date = DateField('Select a Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
