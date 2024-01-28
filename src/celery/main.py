from celery import Celery

from src.celery import config

celery_app = Celery('ECG Analyzer Service',
                    broker=config.RABBITMQ_CONNECTION_STRING,
                    backend=config.REDIS_CONNECTION_STRING)

celery_app.conf.update(**config.config)
celery_app.autodiscover_tasks(['src.celery'])
