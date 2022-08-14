FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt .

COPY entrypoint.sh .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN chmod +x ./entrypoint.sh

COPY . .

ENV PYTHONPATH /usr/src/app
EXPOSE 5005

# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
