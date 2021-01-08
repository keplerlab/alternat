#!/bin/bash
set -e
set -x
docker build --file Dockerfile --tag keplerlab/alternat:0.1.5 .
docker push keplerlab/alternat:0.1.5