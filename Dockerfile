FROM python:3.11.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /myproject

COPY requirements.txt /myproject/
RUN pip install -r requirements.txt

COPY . /myproject/
