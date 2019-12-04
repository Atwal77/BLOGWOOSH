import os
import secrets
from PIL import Image
from Fblog import app,db,mail
from flask import render_template,session,redirect,url_for,flash,request,abort
from flask_bootstrap import Bootstrap
from Fblog.form import loginform,Registerform,UpdateAccountform,Postform,RequestResetForm,ResetPasswordForm,CommentForm,UserForm,FeedbackForm
from flask_bcrypt import Bcrypt
from Fblog.models import User,Post,Comments,Feedback
from Fblog import login_manager
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/home',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def home():
	form=UserForm()
	if form.validate_on_submit():
		return redirect(url_for('user_account',username=form.username.data))
	page = request.args.get('page',1,type=int)
	posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)
	return render_template('bb.html',posts=posts,forms=form)


@app.route('/About')
def About():
 	return render_template('bc.html',title='About')

@app.route('/Contact',methods=['GET','POST'])
def Contact():
	form=FeedbackForm()
	if form.validate_on_submit():
		feedback=Feedback(content=form.content.data)
		db.session.add(feedback)
		db.session.commit()
		flash('Thanks for you valuable feedback!!','success')
		return redirect(url_for('home'))
 	return render_template('feedback.html',title='Contact',form=form,legend='Feeback Form')



@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form=loginform()
	# rform=Registerform()
	if form.validate_on_submit():
		paww=form.password.data
		bcrypt=Bcrypt()
		if User.query.filter_by(email=form.email.data).first():
			user=User.query.filter_by(email=form.email.data).first()
			if bcrypt.check_password_hash(user.password,paww):
				flash('Welcome {} !!'.format(user.username),'success')
				login_user(user,remember=form.remember.data)
				nxt=request.args.get('next')
				# uu=user
				return redirect(nxt) if nxt else redirect(url_for('home'))
			else:
				flash('Wrong username or password','danger')
				return redirect(url_for('login'))

		else:
			flash('Wrong username or password','danger')
			return redirect(url_for('login'))
	return render_template('login.html',forms=form)

def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_picture.filename)
	picture_fn=random_hex + f_ext
	picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)
	output_size=(273,300)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@app.route("/register",methods=['GET','POST'])
def register():
	form=Registerform()
	bcrypt=Bcrypt()
	if form.validate_on_submit():
		hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user=User(username=form.username.data,email=form.email.data,password=hashed_pw,image_file='default.jpg')
		db.session.add(user)
		db.session.commit()
		flash('Account created for {}!'.format(form.username.data),'success')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register',rform=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Your are logged out !!','info')
	return redirect(url_for('home'))

@app.route('/Account',methods=['GET','POST'])
@login_required
def Account():
	form=UpdateAccountform()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file=save_picture(form.picture.data)
			current_user.image_file=picture_file
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Your Account Has Been Updated!','success')
		return redirect(url_for('Account'))
	elif request.method=='GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
	image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
	return render_template('account.html',image=image_file,name=current_user.username,email=current_user.email,form=form)

@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
	form=Postform()
	if form.validate_on_submit():
		post=Post(title=form.title.data,content=form.content.data,author=current_user,date_posted=None,id=None)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!!','success')
		return redirect(url_for('home'))
	return render_template('create_post.html',title='Create_Post',form=form,legend='New Post')


@app.route('/post/<int:post_id>')
def post(post_id):
	post=Post.query.get_or_404(post_id)
	
	return render_template('post.html',post=post)

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
def update_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form=Postform()
	if form.validate_on_submit():
		post.title=form.title.data
		post.content=form.content.data
		db.session.commit()
		flash('Your post has been updated!!','success')
		return redirect(url_for('post',post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data=post.content
	return render_template('create_post.html',legend='Update Post',title='Update Post',form=form,post=post)


@app.route('/post/<int:post_id>/delete',methods=['POST'])
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!!','success')
	return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_posts(username):
	user=User.query.filter_by(username=username).first_or_404()
	page=request.args.get('page',1,type=int)
	posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)
	return render_template('user_posts.html',posts=posts,username=username)

def send_reset_email(user):
	token=user.get_reset_token()
	msg = Message('Password Reset Request',sender='lit2017045@iiita.ac.in',recipients=[user.email])
	msg.body = ''' To reset your password, visit the following link:
{}

If you did not make this request then simply ignore!!
'''.format(url_for('reset_token',token=token,_external=True))

	mail.send(msg)
 


@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form= RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.','info')
		return redirect(url_for('login'))
	return render_template('reset_request.html',title='Reset Password',rform=form)




@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token','warning')
		return redirect(url_for('reset_request'))

	form = ResetPasswordForm()
	bcrypt=Bcrypt()
	if form.validate_on_submit():
		hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pw
		db.session.commit()
		flash('Password Updated for {}!'.format(user.username),'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html',title='Reset Password',rform=form,token=token)



@app.route('/post/<int:post_id>/comments',methods=['GET','POST'])
def comment_post(post_id):
	post = Post.query.get_or_404(post_id)
	form=CommentForm()
	if form.validate_on_submit():
		comment = Comments(content=form.content.data,pcomments=post,author=current_user)
		db.session.add(comment)
		db.session.commit()
		flash('You have commented on this post!!','info')
		return redirect(url_for('comment_post',post_id=post_id))
	return render_template('comments.html',form=form,post=post)



@app.route('/<string:username>')
def user_account(username):
	user = User.query.filter_by(username=username).first()
	if user:
		image_file=url_for('static',filename='profile_pics/'+user.image_file)
		return render_template('user_account.html',image=image_file,name=user.username,email=user.email)
	else:
		abort(404)




@app.route('/post/<int:post_id>/comments/<int:comment_id>/delete',methods=['POST'])
def delete_comment(post_id,comment_id):
	comment=Comments.query.get_or_404(comment_id)
	if comment:
		if comment.author1 != current_user:
			abort(403)
		db.session.delete(comment)
		db.session.commit()
		flash('Your comment has been deleted!!','success')
		return redirect(url_for('comment_post',post_id=comment.post_id))
	else:
		abort(404)

