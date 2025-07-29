from datetime import timedelta
class Config:
    SECRET_KEY = 'CLAVE SECRETA'
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30) 

class Db_Config(Config):
    #MYSQL_HOST = 'localhost'
    #MYSQL_PORT = 3307
    #MYSQL_USER = 'root'
    #MYSQL_PASSWORD = 'Gfl_25030'
    #MYSQL_DB = 'bd_notas'
    #MYSQL_CURSORCLASS = 'DictCursor'  # Para obtener resultados como diccionarios

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Gfl_25030@localhost:3307/bd_notas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


