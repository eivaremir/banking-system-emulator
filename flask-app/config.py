class Config:
    # DEFINIR LLAVE SECRETA PARA GENERAR TOKENS PARA FORMULARIOS
    SECRET_KEY = '12345678'
class DevelopmentConfig(Config):
    DEBUG = True
    PORT='5999'
    

    
    
config ={
    'development':DevelopmentConfig,
    'default':DevelopmentConfig,
    
}
