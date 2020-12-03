#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate alternat
uvicorn message_processor:app --port 8080 --host 0.0.0.0 --reload 2>&1 | tee -a log.txt
