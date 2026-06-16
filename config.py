import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'desenvolvimento-chave-secreta-padrao')
    
    # Supabase fornece URLs que começam com postgres://, mas o SQLAlchemy exige postgresql://
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url or 'sqlite:///parkinson_local.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
