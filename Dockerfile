FROM python:3.9

RUN pip install -U setuptools pip wheel

WORKDIR /checkout
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install .

RUN pip install --no-cache tox

# CMD tox
