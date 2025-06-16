FROM python:3.9-slim

WORKDIR /deguwatch
CMD gunicorn --bind 0.0.0.0:5000 --timeout 50 --workers 2 --worker-class gevent --chdir /deguwatch/app wsgi:application

ADD ./requirements.txt /deguwatch/app/requirements.txt
RUN mkdir -p /deguwatch/data \
    && apt-get update \
    && apt install -y git vim python3-pip libgl1-mesa-glx libglib2.0-0 \
    && apt install -y git vim python3-pip \
    && python3 -m pip install --upgrade pip \
    && pip3 install -r /deguwatch/app/requirements.txt \
    && rm -rf /var/lib/apt/lists/*

ADD . /deguwatch/app
