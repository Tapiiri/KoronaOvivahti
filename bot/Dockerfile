FROM python:3.8

RUN apt update
RUN apt install -y postgresql-client

WORKDIR /code
COPY bot/requirements.txt requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

EXPOSE 22
COPY wait-for-postgres.sh .
CMD [ "python3", "bot/bot.py" ]