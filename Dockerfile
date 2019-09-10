FROM python:3.7.4-slim

ADD . /app
WORKDIR /app

CMD [ "bash", "-l" ]
