from app import create_app
from flask_script import Manager
from config import config

#db

import os

config_class = config['development']

# INSTANCIA DE LA APP CON LAS CONFIGURACIONES
app = create_app(config_class)



if __name__=='__main__':
    #load "database"

    manager = Manager(app)       
    manager.run()
