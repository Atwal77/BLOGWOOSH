from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError,InputRequired
from Fblog.models import User,Post

class loginform(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class Registerform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=50)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')
    def validate_username(self,username):
    	user=User.query.filter_by(username=username.data).first()
    	if user:
    		raise ValidationError('That username is already taken,Please choose another one !!')

    def validate_email(self,email):
    	email=User.query.filter_by(email=email.data).first()
    	if email:
    		raise ValidationError('That email is already taken,Please choose another one !!')



class UpdateAccountform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=100)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')
    def validate_username(self,username):
    	if username.data != current_user.username:
    		user=User.query.filter_by(username=username.data).first()
    		if user:
    			raise ValidationError('That username is already taken,Please choose another one !!')

    def validate_email(self,email):
    	if email.data != current_user.email:
    		email=User.query.filter_by(email=email.data).first()
    		if email:
    			raise ValidationError('That email is already taken,Please choose another one !!')



class Postform(FlaskForm):
    title=StringField('Title',validators=[DataRequired(),Length(min=2,max=50)])
    content=TextAreaField('Content',validators=[DataRequired()],render_kw={'class': 'form-control', 'rows': 10})
    submit=SubmitField('Post')



class RequestResetForm(FlaskForm):
	email=StringField('Email',validators=[DataRequired(),Email()])
	submit=SubmitField('Request Password Reset')
	def validate_email(self,email):
	    email=User.query.filter_by(email=email.data).first()
    	if email is None:
    		raise ValidationError('There is no account with that email. You must register first!!')





class ResetPasswordForm(FlaskForm):
	password=PasswordField('Password',validators=[DataRequired()])
	confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField('Reset Password')



class CommentForm(FlaskForm):
    content=TextAreaField('Content',validators=[DataRequired()],render_kw={'class': 'form-control', 'rows': 4})
    submit=SubmitField('Comment')


class UserForm(FlaskForm):
	username = TextAreaField('Content',validators=[DataRequired()],render_kw={'class': 'form-control', 'rows': 1})
	submit = SubmitField('Submit')


class FeedbackForm(FlaskForm):
	title=StringField('Title',validators=[DataRequired(),Length(min=2,max=50)])
	content=TextAreaField('Content',validators=[DataRequired()],render_kw={'class': 'form-control', 'rows': 10})
	submit=SubmitField('Post')