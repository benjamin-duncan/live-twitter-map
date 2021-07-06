FROM python:3.8
WORKDIR /app
COPY requirements.txt /app
RUN apt-get update &&\
apt-get install -y python-dev &&\ 
apt-get clean
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY entrypoint.sh/ /
COPY . /app
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /var/run/celery /var/log/celery
RUN chown -R nobody:nogroup /var/run/celery /var/log/celery