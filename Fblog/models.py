from Fblog import db,app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

class User(db.Model,UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),unique=True)
	email=db.Column(db.String(120),unique=True,nullable=False)
	image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
	password=db.Column(db.String(60),nullable=False)
	posts=db.relationship('Post',backref='author',lazy=True)
	comments=db.relationship('Comments',backref='author1',lazy=True)

	# def __repr__(self):
	# 	return "User('{0}','{1}','{2}')".format(self.username,self.email,self.image_file)
	def __init__(self,username,image_file,email,password):
		self.username=username
		self.email=email
		self.image_file=image_file
		self.password=password
		# self.posts=posts

	def get_reset_token(self,expires_sec=1800):
		s= Serializer(app.config['SECRET_KEY'],expires_sec)
		return s.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s=Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)


class Post(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(100),nullable=False)
	date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	content=db.Column(db.Text,nullable=False)
	comments=db.relationship('Comments',backref='pcomments',lazy=True)
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	# def __repr__(self):
	# 	return "Post('{0}','{1}')".format(self.title,self.date_posted)
	def __init__(self,id,title,date_posted,content,author):
		self.id=id
		self.title=title
		self.date_posted=date_posted
		self.content=content
		self.user_id=author.id



class Comments(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	content=db.Column(db.Text,nullable=False)
	post_id=db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
	user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

	def __init__(self,content,pcomments,author):
		self.content=content
		self.post_id=pcomments.id
		self.user_id=author.id

class Feedback(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	content=db.Column(db.Text,nullable=False)


	def __init__(self,content):
		self.content=content