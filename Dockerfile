FROM python:3.11-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt

COPY . /usr/src/app/

CMD ["python", "main.py"]
