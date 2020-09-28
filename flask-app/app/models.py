#from . import db # import from module app
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

from flask_login import UserMixin

def showPasswordHash(value):
    return generate_password_hash(value)

'''
class Task(db.Model):
    __tablename_ = 'tasks'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime)

    @property
    def little_description(self):
        if len(self.description)>40: return self.description[0:39]+"..."
        return self.description

    @classmethod 
    def create_element(cls, title, desc, user_id):
        task = Task(title=title,description=desc, user_id=user_id)
        db.session.add(task)
        db.session.commit()
        return task
    @classmethod
    def get_by_id(cls, id):
        
        # busca la línea en la bd
        return Task.query.filter_by(id=id).first()
    
    @classmethod
    def update_element(cls, id, title, description):
        
        # busca la línea task en la base de datos segun la información de la vista
        task = Task.get_by_id(id)

        # si ese objeto no existe...
        if task is None:
            return False
        
        # si el objeto existe... modifica la línea con la información de la vista
        task.title = title
        task.description = description

        # aplica los cambios en la bd
        db.session.add(task)
        db.session.commit()
        
        return task
    @classmethod
    def delete_element(cls,id):
        task = Task.get_by_id(id)
        if task is None: return False
        db.session.delete(task)
        db.session.commit()
        return True
    

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    # campos de la tabla
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique = True, nullable=False)
    password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now())
   

    def verify_password(self,p_password):
        return check_password_hash(self.password, p_password)
    @property
    def passwd(self):
        pass
    @passwd.setter
    def passwd(self, value):
        self.password = generate_password_hash(value)

    def __str__(self):
        return self.username
    
    @classmethod
    def create_element(cls,username,password,email):
        user = User(username=username,passwd=password,email=email)
        
        # registrar nueva entrada en la BD
        db.session.add(user)

        # registramos acciones
        db.session.commit()
        return user
    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()
    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()
    @classmethod
    def get_by_id(cls, id):
        return User.query.filter_by(id=id).first()
'''