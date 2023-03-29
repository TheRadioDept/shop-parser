FROM python:3.10

WORKDIR /webparse-app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /webparse-app
