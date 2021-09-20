import os
SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))

# DB setting
DB_HOST = os.getenv('DB_HOST','127.0.0.1:5432')
DB_USER = os.getenv('DB_USER','postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD','tony55637')
DB_NAME = os.getenv('DB_NAME', 'capstone_movie')
DB_PATH = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

SQLALCHEMY_DATABASE_URI = DB_PATH