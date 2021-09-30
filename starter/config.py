import os
SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))

# DB setting
DB_HOST = os.getenv('DB_HOST','127.0.0.1:5432')
DB_USER = os.getenv('DB_USER','postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD','tony55637')
DB_NAME = os.getenv('DB_NAME', 'capstone_movie')
DB_NAME_TEST = os.getenv('DB_NAME', 'capstone_movie_test')
DB_PATH = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
DB_PATH_TEST = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_TEST}'

# DB_PATH = 'postgresql://soonxhmzrddqnx:8a2dca8b7741fce23d4d5311c2dce5273a6308ef105ae3bd6056b4b8027c77c8@ec2-34-233-187-36.compute-1.amazonaws.com:5432/df1lf4nk1ose1m'


SQLALCHEMY_DATABASE_URI = DB_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False


# AUTH TOKEN
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN', None)
ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN', None)
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN', None)