import os

RABBITMQ_CONNECTION_STRING = os.getenv('RABBITMQ_CONNECTION_STRING')
REDIS_CONNECTION_STRING = os.getenv('REDIS_CONNECTION_STRING')

QUEUE_ECG_ANALYSIS = 'ecg_analyzer'
QUEUE_DB_TRANSACTIONS = 'db_transactions'

config = {
    'task_serializer': 'pickle',
    'result_serializer': 'pickle',
    'result_backend_transport_options': {
        'global_keyprefix': 'ecg:'
    },
    'redis_retry_on_timeout': True,
    'accept_content': ['application/json', 'application/x-python-serialize'],
    'task_acks_late': True,
    'broker_connection_retry_on_startup': True,
    'task_routes': {
        'src.celery.tasks.async_analyze_ecg_leads': {
            'queue': QUEUE_ECG_ANALYSIS,
            'routing_keys': QUEUE_ECG_ANALYSIS,
            'queue_arguments': {'x-queue-mode': 'lazy'}
        },
        'src.celery.tasks.async_analyze': {
            'queue': QUEUE_ECG_ANALYSIS,
            'routing_keys': QUEUE_ECG_ANALYSIS,
            'queue_arguments': {'x-queue-mode': 'lazy'}
        },
        'src.celery.tasks.async_count_zero_crosses': {
            'queue': QUEUE_ECG_ANALYSIS,
            'routing_keys': QUEUE_ECG_ANALYSIS,
            'queue_arguments': {'x-queue-mode': 'lazy'}
        },
        'src.celery.tasks.async_ecg_create': {
            'queue': QUEUE_DB_TRANSACTIONS,
            'routing_keys': QUEUE_DB_TRANSACTIONS,
            'queue_arguments': {'x-queue-mode': 'lazy'}
        },
        'src.celery.tasks.async_ecg_create_analysis': {
            'queue': QUEUE_DB_TRANSACTIONS,
            'routing_keys': QUEUE_DB_TRANSACTIONS,
            'queue_arguments': {'x-queue-mode': 'lazy'}
        },
        'src.celery.tasks.async_ecg_update_analysis_by_id': {
            'queue': QUEUE_DB_TRANSACTIONS,
            'routing_keys': QUEUE_DB_TRANSACTIONS,
            'queue_arguments': {'x-queue-mode': 'lazy'}
        }
    }
}
