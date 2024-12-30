from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo
from flask_ckeditor import CKEditorField


class DateForm(FlaskForm):
    date = DateField('Select a Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
