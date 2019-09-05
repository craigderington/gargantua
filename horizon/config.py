import os

# app settings 
SECRET_KEY = os.urandom(64)
DEBUG = True

# celery Settings
CELERY_BROKER_URL = "pyamqp://rabbitmq:5672/"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
TASK_SERIALIZER = "json"
RESULT_SERIALZIER = "json"
ACCEPT_CONTENT = ["json"]

# sqlalchemy 
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "sqlite:///gargantua.db"

# timezome
TIMEZONE = "America/New_York"
ENABLE_UTC = True

