import os
from functools import partial
import psycopg2
from telegram.ext import Updater
import logging

import handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

conn = psycopg2.connect(
    f"host={os.environ['POSTGRES_HOST']} \
        dbname={os.environ['POSTGRES_DB']} \
        password={os.environ['POSTGRES_PASSWORD']} \
        user={os.environ['POSTGRES_USER']}")

updater = Updater(
    token=os.environ['ADMINBOT_TOKEN'], use_context=True)

dispatcher = updater.dispatcher

for module in handlers.__all__:
    dispatcher.add_handler(getattr(handlers, module).handler(conn))

updater.start_polling()
