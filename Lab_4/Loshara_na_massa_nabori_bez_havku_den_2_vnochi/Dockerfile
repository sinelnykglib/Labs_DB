FROM python:3.8

WORKDIR /usr/src/Loshara_na_massa_nabori_bez_havku_den_2_vnochi
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/Loshara_na_massa_nabori_bez_havku_den_2_vnochi/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libpq-dev
COPY . /usr/src/Loshara_na_massa_nabori_bez_havku_den_2_vnochi/

CMD ["python", "DB_lab2.py"]
