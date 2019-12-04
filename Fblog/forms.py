from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from Fblog.models import User,Post

class loginform(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')


class Registerform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
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


class Registerform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
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



class Registerform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
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