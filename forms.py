from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo
from flask_ckeditor import CKEditorField


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone Number', render_kw={"placeholder": "Phone Number"})
    message = CKEditorField('Message', validators=[DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField('Submit')


class DateForm(FlaskForm):
    date = DateField('Select a Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
