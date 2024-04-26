FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /anverali

COPY requirements.txt /anverali/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /anverali/