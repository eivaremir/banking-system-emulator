#from . import db # import from module app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import random
import abc
#from flask_login import UserMixin

prueba = lambda s: s if (len(df_transactions[df_transactions['id']==s])) == 0 else prueba(random.choice(range(100000,999999)))
def showPasswordHash(value):
    return generate_password_hash(value)

class Product(abc.ABC):
  @abc.abstractmethod
  def __init__(self,**kwargs):
    self._id = kwargs['id']
    self._interest_rate = kwargs['interest_rate']
    self._balance = 0.00
  @property
  def interest_rate(self):
    return self._interest_rate
  @property
  def id(self):
    return self._id
  @property
  def balance(self):
    return self._balance

  def to_dict(self):
    return {
      'id': self._id,
      'interest_rate': self._interest_rate,
      'balance': self.balance
    }
  @classmethod
  def getProductBalance(**kwargs):
    id = kwargs['id']


  def __repr__(self):
    return self.__class__.__name__+"("+self._id+", interest_rate="+str(self._interest_rate)+", Balance ="+str(self._balance)+")"

class SavingAccount(Product):
  def __init__(self,**kwargs): 
    super().__init__(**kwargs)
  
class FixedTermDeposit(Product):
  def __init__(self,**kwargs): 
    super().__init__(**kwargs)

class Loan(Product):
  def __init__(self,**kwargs): 
    super().__init__(**kwargs)
    # duracion del prestamo en meses
    self.length = kwargs['length']

    # base del calculo
    self.base = kwargs['base']
  def to_dict(self):
    d1 = super().to_dict()
    d2 = {
        "length":self.length,
        "base":self.base
    }
    return {**d1,**d2}

class CreditCard(Product):
  def __init__(self,**kwargs): 
    super().__init__(**kwargs)

class Client():
  def __init__(self, **kwargs):
    self.id = kwargs['id']
    self.name = kwargs['name']
    self.products = kwargs['products']
  def __repr__(self):
    return "Client("+self.id+", "+self.name+", products="+str(len(self.products))+")"

class Transaction():
  def __init__(self,**kwargs):
    self._id = kwargs['id']
    #Dr/Cr
    self.nature = kwargs['nature']
    self.accounting_date = kwargs['date']
    self.amount = kwargs['amt']
    self.product = kwargs['product']
    self.mvt = kwargs['mvt']
    
  def __repr__(self):
    return self.__class__.__name__+"("+str(self._id)+","+self.accounting_date.strftime("%A, %B %d %Y")+", "+self.nature+", "+str(self.amount) +")"
  def to_dict(self):
    return {
      'id': self._id,
      'nature': self.nature,
      'accounting_date':self.accounting_date,
      'amount':self.amount,
      'product':self.product,
      'mvt': self.mvt
    }

class Transfer():
  def __init__(self, **kwargs):
    self.to = kwargs['to']
    self.From = kwargs['from']
    self.amount = kwargs['amount']
    self._id = kwargs['id']

  def __repr__(self):
    return self.__class__.__name__+"("+self.to+","+self.From+", "+self._id+", "+self.amount +")"  
    
  def to_dict(sefl):
    return {
        'to': self.to,
        'From': self.From,
        'amount': self.amount,
        'id': self._id,
        'date': self.accounting_date
    }
  
  @classmethod
  def Execute(self, **kwargs):
    print("Executing Bank Transfer")
    b1 = df_deposits[df_deposits['id']==kwargs['to']]

    b2 = df_deposits[df_deposits['id']==kwargs['From']]
    if len(b1) == 0 or len(b2) == 0:
      print('ERROR')
    else: 
      b1 = b1.reset_index()
      b1 = b1.iloc[0]['balance']
      b2 = b2.reset_index()
      b2 = b2.iloc[0]['balance']
      print("Saldo disponible:",b2)
      if b2 >= kwargs['amount']:
        totalb1= b1 + kwargs['amount']
        totalb2= b2 - kwargs['amount']
        trans1= Transaction(
          id = prueba(random.choice(range(100000,999999))),
          product = kwargs['to'],
          nature = "Cr",
          date = datetime.now(),
          amt = kwargs['amount'],
          mvt = kwargs['amount'])
        trans2= Transaction(
          id = prueba(random.choice(range(100000,999999))),
          product = kwargs['From'],
          nature = "Dr",
          date = datetime.now(),
          amt = kwargs['amount'],
          mvt= kwargs['amount']*-1)
        global df_transactions
        df_transactions = df_transactions.append(trans1.to_dict(),ignore_index=True )
        df_transactions = df_transactions.append(trans2.to_dict(),ignore_index=True )
       
      else:
        print("No tienes saldo")


    
      



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