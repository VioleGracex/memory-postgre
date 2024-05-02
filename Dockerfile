FROM python:3.11.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /myproject
RUN pip install --upgrade pip
COPY requirements.txt /myproject/
RUN pip install -r requirements.txt

COPY . /myproject/

EXPOSE 8088