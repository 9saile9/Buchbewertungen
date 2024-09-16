import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'erraetst-Du-nie'
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        POSTS_PER_PAGE = 10
        
        
