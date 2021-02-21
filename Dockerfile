FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# Dockerfile for testing the app

COPY app/ /app/app
COPY tests/ /app/tests
COPY requirements.txt /app/requirements.txt
COPY .coveragerc /app/.coveragerc
COPY requirements-dev.txt /app/requirements-dev.txt
COPY prestart.sh /app/prestart.sh

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
