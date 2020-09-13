FROM python:3.8

WORKDIR /code
COPY bot/requirements.txt requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

EXPOSE 22
COPY bot/ .
COPY botlib .

CMD [ "python3", "bot.py" ]