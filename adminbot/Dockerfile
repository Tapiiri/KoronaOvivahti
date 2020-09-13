FROM python:3.8

RUN apt update
RUN apt install -y postgresql-client

WORKDIR /code
COPY adminbot/requirements.txt requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

EXPOSE 22
COPY adminbot/ .
COPY botlib .
COPY wait-for-postgres.sh .

CMD [ "python3", "adminbot.py" ]