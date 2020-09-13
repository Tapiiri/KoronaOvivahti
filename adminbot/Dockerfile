FROM python:3.8

WORKDIR /code
COPY adminbot/requirements.txt requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

EXPOSE 22
COPY adminbot/ .
COPY botlib .

CMD [ "python3", "adminbot.py" ]