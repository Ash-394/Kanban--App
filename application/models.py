import email
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True,nullable=False,autoincrement=True,unique = True)
    username = db.Column(db.String, db.ForeignKey('user.id'),nullable = False)
    task = db.Column(db.String,nullable = False)
    title = db.Column(db.String,nullable = False)
    status = db.Column(db.Integer, db.ForeignKey('list.id'), nullable = False) #list name
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    due_date = db.Column(db.Date())
    completed = db.Column(db.String)
    completed_date = db.Column(db.DateTime(timezone=True))

class List(db.Model):
    id = db.Column(db.Integer,primary_key = True, nullable = False, unique = True ,autoincrement=True)
    list_name = db.Column(db.String,nullable = False,unique = False)
    username = db.Column(db.String, db.ForeignKey('user.id'),nullable = False)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    lists = db.relationship('List')
    tasks = db.relationship('Tasks')


 



