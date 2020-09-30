#from . import db # import from module app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import random
import abc
import string
import numpy as np
#from model.ipynb* import *
try:
  from .functions import *
  DATABASE_DIRECTORY = os.getcwd()+"/app/db/"
except:
  from functions import *
  DATABASE_DIRECTORY = os.getcwd()+"/db/"
#from flask_login import UserMixin
df_transactions = pd.read_csv(DATABASE_DIRECTORY+'transactions.csv',parse_dates=['accounting_date'])
df_deposits = pd.read_csv(DATABASE_DIRECTORY+"deposits.csv")


def showPasswordHash(value):
    return generate_password_hash(value)

class Product(abc.ABC):
  @abc.abstractmethod
  def __init__(self,**kwargs):
    self._id = kwargs['id']
    self._interest_rate = kwargs['interest_rate']
    
    try:
      self._balance = kwargs['balance']
    except:
      self._balance = 0.00
    self._owner = kwargs['owner']
  @property
  def owner(self):
    return self._owner
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
      'balance': self.balance,
      'owner':self._owner,
      'type':self.__class__.__name__
    }
  @classmethod
  def getProductBalance(self,**kwargs):
    df_transactions = pd.read_csv(DATABASE_DIRECTORY+'transactions.csv',parse_dates=['accounting_date'])
    df_deposits = pd.read_csv(DATABASE_DIRECTORY+"deposits.csv")
    df_loans = pd.read_csv(DATABASE_DIRECTORY+"loans.csv")
    id = kwargs['id']
    
    try: balance = df_deposits[df_deposits.id == id].iloc[0]['balance']
    except: pass
    try: balance = df_loans[df_loans.id == id].iloc[0]['balance']
    except: pass

    return balance



  def __repr__(self):
    return self.__class__.__name__+"("+self._id+", interest_rate="+str(self._interest_rate)+", Balance ="+str(self._balance)+")"

class SavingAccount(Product):
  def __init__(self,**kwargs): 
    super().__init__(**kwargs)
    self.type = self.__class__.__name__
  
class FixedTermDeposit(Product):
  def __init__(self,**kwargs): 
    super().__init__(**kwargs)
    self.type = self.__class__.__name__

class Loan(Product):
  def __init__(self,**kwargs): 
    super().__init__(**kwargs)
    # duracion del prestamo en meses
    self.length = kwargs['length']
    self.type = self.__class__.__name__
    # base del calculo
    self.base = kwargs['base']

  
  def generate_amortization_table(self):
    arr = np.array([])
    for i in range(self.length):
      arr = np.append(arr,(self.balance*(self.interest_rate/100)*30)/self.base)
    return arr,arr.sum()

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
    self.type = self.__class__.__name__

class Client():
  def __init__(self, **kwargs):
    self.id = kwargs['id']
    self.name = kwargs['name']
    self.products = kwargs['products']
  def __repr__(self):
    return "Client("+self.id+", "+self.name+", products="+str(len(self.products))+")"
  def to_dict(self):
    return {
      "id":self.id,
      "client_name":self.name
    }
  @classmethod 
  def getClientData(self,**kwargs):
    df_clients =pd.read_csv(DATABASE_DIRECTORY+"clients.csv")
    return df_clients[df_clients.id == kwargs['client']]

  @classmethod
  def getClientProducts(self,**kwargs):
    df_deposits = pd.read_csv(DATABASE_DIRECTORY+"deposits.csv")
    df_loans = pd.read_csv(DATABASE_DIRECTORY+"loans.csv")

    client_deposits = df_deposits[df_deposits.owner == kwargs['client']]
    client_loans = df_loans[df_loans.owner==kwargs['client']]

    client_products = []
    for i in range(len(client_deposits)):
        #print(client_deposits.iloc[i].type)
        if eval(client_deposits.iloc[i].type) == SavingAccount:
            client_products.append(SavingAccount(
                id = str(client_deposits.iloc[i].id),
                interest_rate = client_deposits.iloc[i].interest_rate,
                balance = float(client_deposits.iloc[i].balance),
                owner = client_deposits.iloc[i].owner,
                type = client_deposits.iloc[i].type
            ))
        if eval(client_deposits.iloc[i].type) == FixedTermDeposit:
            client_products.append(FixedTermDeposit(
                id = str(client_deposits.iloc[i].id),
                interest_rate = client_deposits.iloc[i].interest_rate,
                balance = float(client_deposits.iloc[i].balance),
                owner = client_deposits.iloc[i].owner,
                type = client_deposits.iloc[i].type
            ))
    for i in range(len(client_loans)):

        client_products.append(Loan(
                id = str(client_loans.iloc[i].id),
                interest_rate = client_loans.iloc[i].interest_rate,
                balance = float(client_loans.iloc[i].balance),
                owner = client_loans.iloc[i].owner,
                length = client_loans.iloc[i].length,
                base = client_loans.iloc[i].base,
                type = client_loans.iloc[i].type
        ))
    return client_products
    

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
          id = id_in_table(random.choice(range(100000,999999))),
          product = kwargs['to'],
          nature = "Cr",
          date = datetime.now(),
          amt = kwargs['amount'],
          mvt = kwargs['amount'])
        trans2= Transaction(
          id = id_in_table(random.choice(range(100000,999999))),
          product = kwargs['From'],
          nature = "Dr",
          date = datetime.now(),
          amt = kwargs['amount'],
          mvt= kwargs['amount']*-1)
        global df_transactions
        df_transactions = df_transactions.append(trans1.to_dict(),ignore_index=True )
        df_transactions = df_transactions.append(trans2.to_dict(),ignore_index=True )
        if kwargs['to'] == Product_in_loan(kwargs['to']):
          prodct1 = Product(
              id = kwargs['to'],
              interest_rate = GetInteresLOANS(kwargs['to']),
              balance = totalb1,
              length = GetLengthLOANS(kwargs['to']),
              base = GetBaseLOANS(kwargs['to']))
          df_loans = df_loans.append(product1.to_dict(),ignore_index=True)
        elif kwargs['to'] == Product_in_deposits(kwargs['to']):
          product1 = Product(
              id = kwargs['to'],
              interest_rate = GetInteres(kwargs['to']),
              balance = totalb1)
          df_deposits = df_deposits.append(product1.to_dict(),ignore_index=True)

        elif kwargs['FROM'] == Product_in_deposits(kwargs['FROM']):    
          product2 = Product(
              id = kwargs['FROM'],
              interest_rate = GetInteres(kwargs['FROM']),
              balance = totalb2)
          df_deposits = df_deposits.append(product2.to_dict(),ignore_index=True)
        elif kwargs['FROM'] == Product_in_CC(kwargs['FROM']): 
          product2 = Product(
              id = kwargs['FROM'],
              interest_rate = GetInteresCC(kwargs['FROM']),
              balance = totalb2)
          df_CreditCrad = df_CreditCrad.append(product2.to_dict(),ignore_index=True)
      else:
        print("No tienes saldo")


    
      

class User(UserMixin):

    # campos de la tabla
    id = 1
    username = 'admin'
    password = 'pbkdf2:sha256:150000$qdu0Y5KT$200e4fb764e337538b096571845b058258fabba32bf20a94659768779bd10113'
    
    def verify_user(self,user):
      return user==self.username
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
    
    
    '''
    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()
    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()
    '''
    @classmethod
    def get_by_id(cls, id):
        return 1
    
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