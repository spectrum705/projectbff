from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, widgets, SelectField
from wtforms.validators import DataRequired,Length, EqualTo, ValidationError
from message import db
from flask_mongoengine.wtf import model_form
from flask_ckeditor import CKEditorField



class LoginForm(FlaskForm):
    username = StringField('Your Username',
                        validators=[DataRequired(),
                    Length(min = 3, max= 15 ) ])
    password = PasswordField('Your Password', 
                    validators = [DataRequired()])
    submit = SubmitField('Login')

class WriteForm(FlaskForm):
    receiver = SelectField('Select receiver', validators=[DataRequired()],  render_kw={"placeholder": "Who are you sending?"})
    def validate_receiver(form, field):
        if field.data == '':
            raise ValidationError('Please select a valid partner as the receiver.')
    title = StringField('Title..',
                validators=[DataRequired()], render_kw={"placeholder": "Enter Title"})
    content = TextAreaField('write your letter here :)', 
            validators = [DataRequired()],  render_kw={"placeholder": "write your letter here :)"})
    # content = CKEditorField('write your letter here :)',validators = [DataRequired()],  render_kw={"placeholder": "write your letter here :)"})
    submit = SubmitField('Send >')
    
class NewUserForm(FlaskForm):
    username = StringField('Your Username',
                        validators=[DataRequired(),
                    Length(min = 3, max= 15 ) ])
    
    password = PasswordField('Your Password', 
                    validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    partners = SelectMultipleField('Select your Partners', coerce=str, render_kw={"size": 5}, option_widget=widgets.CheckboxInput(),
       widget=widgets.ListWidget(prefix_label=False))

    mobile = StringField('Your Number if you want to get sms', render_kw={"placeholder": "+91... (optional)"})
    submit = SubmitField('Create')
