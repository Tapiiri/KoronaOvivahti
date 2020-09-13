FROM python:3.8

WORKDIR /code
COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

EXPOSE 22
COPY . .

CMD [ "python3", "src/bot.py" ]