from ..settings import *

ALLOWED_HOSTS = ['server.mall.thairod.care', '202.151.188.165']

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    'https://mall.thairod.care',
]

FRONTEND_URL = "https://mall.thairod.care/"

CELERY_BROKER_URL = 'amqp://rabbitmq'
