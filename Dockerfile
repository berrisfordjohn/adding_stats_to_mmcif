FROM python:3.9-alpine

RUN apk add --update --no-cache g++ 

RUN pip install -U setuptools pip wheel

WORKDIR /checkout
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install .
