FROM python:3.13.2

RUN mkdir /backend
WORKDIR /backend

RUN apt update && apt install -y postgresql-client postgresql

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend

RUN groupadd -r testuser && useradd -r -g testuser testuser
USER testuser