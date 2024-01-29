from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, widgets, SelectField, FileField, MultipleFileField, EmailField, DateField
from wtforms.validators import DataRequired,Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
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

class FeedbackForm(FlaskForm):
    feedback= TextAreaField( 
            validators = [DataRequired()],  render_kw={"placeholder": "Please write your Feedback :)"})
    subject =  StringField('Title..',
                validators=[DataRequired()], render_kw={"placeholder": "Enter Subject"})
    submit = SubmitField('Send >')

class WriteForm(FlaskForm):
    
    receiver = SelectField('Select receiver', validators=[DataRequired()],  render_kw={"placeholder": "Who are you sending?"})
    def validate_receiver(form, field):
        if field.data == '':
            raise ValidationError('Please select a valid partner as the receiver.')
    title = StringField('Title..',
                validators=[DataRequired()], render_kw={"placeholder": "Title"})
    # TODO add info about image pasting. test rich text editor too
    content = TextAreaField( 
            validators = [DataRequired()],  render_kw={"placeholder": "write your letter here :)"})
    # content = CKEditorField('write your letter here :)',validators = [DataRequired()],  render_kw={"placeholder": "write your letter here :)"})
    # images = FileField('Your images', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    images = MultipleFileField('Your images', validators=[FileAllowed(['jpg', 'png', 'gif','jpeg'], 'Images only!')],render_kw={"placeholder": "Add Images?"})
    submit = SubmitField('Send >')
    
    

class NewUserForm(FlaskForm):
    username = StringField('Your Username',
                        validators=[DataRequired(),
                    Length(min = 3, max= 15 ) ])
    # birthday= DateField('When is your Birthday?', validators=[DataRequired()] ,  format="%m-%d")
    password = PasswordField('Your Password', 
                    validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # partners = SelectMultipleField('Select your Partners', coerce=str, render_kw={"size": 5}, option_widget=widgets.CheckboxInput(),
    #    widget=widgets.ListWidget(prefix_label=False))
    friend_code=StringField('Enter Friend Code',
                        validators=[Length(max=4 ) ])#,render_kw={"placeholder":"Have your Friend's Code?"})
    mobile = StringField('Your Number if you want to get sms', render_kw={"placeholder": "+91... (optional)"})
    email = EmailField("Email ID",render_kw={"placeholder":"Your Email ID (required)"})
    # email = StringField()
    submit = SubmitField('Create')

class AddFriendForm(FlaskForm):
    code_firstDigit=StringField('Enter Friend Code',
                        validators=[DataRequired(),
                    Length(max=1 ) ])
    code_secondDigit=StringField('Enter Friend Code',
                validators=[DataRequired(),
            Length(max=1 ) ])
    code_thirdDigit=StringField('Enter Friend Code',
                validators=[DataRequired(),
            Length(max=1 ) ])
    code_fourthDigit=StringField('Enter Friend Code',
                        validators=[DataRequired(),
                    Length(max=1 ) ])
    
    submit = SubmitField('Add Partner')