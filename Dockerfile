FROM python:3.10-slim

WORKDIR /bot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r /bot/requirements.txt

COPY ./alembic.ini alembic.ini
COPY ./alembic alembic

COPY startup.sh .
# RUN dos2unix startup.sh
RUN chmod +x startup.sh

COPY ./src src

EXPOSE 3001