#! /bin/bash
celery -A src.celery.main worker -E \
     --without-heartbeat --without-gossip --without-mingle -Ofair \
     --loglevel=INFO --uid=nobody --gid=nogroup \
     -Q "${CELERY_ANALYZER_QUEUE}","${CELERY_DB_TRANSACTIONS_QUEUE}"