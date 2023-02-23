from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length, EqualTo, ValidationError
from message import db
from flask_mongoengine.wtf import model_form


class LoginForm(FlaskForm):
    username = StringField('Your Username',
                        validators=[DataRequired(),
                    Length(min = 3, max= 15 ) ])
    password = PasswordField('Your Password', 
                    validators = [DataRequired()])
    submit = SubmitField('Login')

class WriteForm(FlaskForm):
    title = StringField('Title..',
                validators=[DataRequired()], render_kw={"placeholder": "Enter any Title"})
    content = TextAreaField('write your letter here :)', 
            validators = [DataRequired()],  render_kw={"placeholder": "write your letter here :)"})
    submit = SubmitField('Send >')