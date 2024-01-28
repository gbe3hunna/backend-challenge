#! /bin/bash
sleep 10
uvicorn src.api.main:app \
     --host 0.0.0.0 \
     --port 8000 \
     --workers "${UVICORN_API_WORKERS}"