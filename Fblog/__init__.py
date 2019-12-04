import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)
app.config['SECRET_KEY']='\xca6\xe4\xd1\xd4\t\x080\xb3\xfc\xbb\xa4\xcab\x15\xe5'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:Harjot12$@localhost/userposts'
db=SQLAlchemy(app)
boot=Bootstrap(app)
manager=Manager(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='lit2017045@iiita.ac.in'
app.config['MAIL_PASSWORD']='makhanshahs'
mail = Mail(app) 


from Fblog.models import User,Post
from Fblog import routes

# beautifully recovered the circular imports as __init__.py is not __main__ hence it is saved from circular import #