from ..settings import *

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://mall.dev.thairod.care",
    "https://mall.dev.thairod.care",
]

FRONTEND_URL = "https://mall.dev.thairod.care/"

CELERY_BROKER_URL = 'amqp://rabbitmq'
