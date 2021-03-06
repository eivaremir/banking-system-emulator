import pandas as pd
import random
import os
#from model.ipynb* import *
print(os.getcwd())
try:
  from .models import *
  
  DATABASE_DIRECTORY = os.getcwd()+"/app/db/"
except:
  from models import *
  DATABASE_DIRECTORY = os.getcwd()+"/db/"

def load_clients():
  print("Getting Clients...")
  return pd.read_csv(DATABASE_DIRECTORY+"clients.csv")
def getAccountStatement(**kwargs):
  df_transactions = pd.read_csv(DATABASE_DIRECTORY+'transactions.csv',parse_dates=['accounting_date'])
  df_deposits = pd.read_csv(DATABASE_DIRECTORY+"deposits.csv")

  try: kwargs['product']
  except: print("A product id is required")

  
  print("Getting account statement for product",kwargs['product'])
  
  df = df_transactions[df_transactions['product'] == kwargs['product']]
  
  try: start = kwargs['start'] 
  except: start = df['accounting_date'].min()
  try: end = kwargs['end']
  except: end = df['accounting_date'].max()
  
  df = df[(df.accounting_date >= start) & (df.accounting_date <= end) ]

  print("Found",len(df),"transactions from",start,"to",end)
  df = df.sort_values(by=['accounting_date'])
  df = df.reset_index()
  df = df.drop(['index'],axis=1)
  return df

id_in_table = lambda s: s if (len(df_transactions[df_transactions['id']==s])) == 0 else id_in_table(random.choice(range(100000,999999)))

def generate_product_ids():
  id = ''
  while (id in ids or id == ''):
    id = str(random.choice(range(1000000,9999999)))
  product_ids.append(id)
  return id   


def generate_credit_card_number():
  id = ''
  while (id in ids or id == ''):
    id = str(random.choice(range(1000000000000000,9999999999999999)))
  product_ids.append(id)
  return id   


def generate_transaction_id():
  id = ''
  while (id in ids or id == ''):
    id = str(random.choice(range(100000,9999999)))
  transaction_ids.append(id)
  return id   


def generate_client_id():
  id = ''
  while (id in ids or id == ''):
    id = str(random.choice(range(1,11)))+"-"+ str(random.choice(range(100,999)))+"-"+ str(random.choice(range(1,999)))
  ids.append(id)
  return id   

def generate_saving_accounts(n):
  accs = []
  for i in range(n):
    accs.append(SavingAccount(
        id = generate_product_ids()
    ))
  return accs

def generate_clients(n):
  clients = []
  for i in range(n):
    clients.append(Client(
        id = generate_client_id(),
        name = rand_str(10) +" "+rand_str(15),
        products = []
    ))
  return clients

def generate_balance():
  n = random.choice(range(0,500000))
  cash= ("${:5.2f}".format(n))
  return cash
