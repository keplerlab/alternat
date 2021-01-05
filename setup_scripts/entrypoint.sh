#!/bin/bash
source /venv/bin/activate && cd ./api/ && uvicorn message_processor:app --port 8080 --host 0.0.0.0 --reload 2>&1 | tee -a log.txt
