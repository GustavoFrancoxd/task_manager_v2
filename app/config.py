from datetime import timedelta
class Config:
    SECRET_KEY = 'CLAVE SECRETA'
    DEBUG = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30) 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Gfl_25030@localhost:3307/bd_notas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
