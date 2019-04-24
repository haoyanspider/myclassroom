import os
SECRET_KEY = os.urandom(24)
DEBUG = 'True'

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'haoyan'
HOST = '127.0.0.1'
POST = '3306'
DATABASE = 'zhiliao'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset urf8'.format(DIALECT, DRIVER, USERNAME,
                                                                       PASSWORD, HOST, POST, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
