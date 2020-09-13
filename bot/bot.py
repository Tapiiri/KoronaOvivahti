import os
from functools import partial
import psycopg2
from telegram.ext import Updater
import logging

import handlers
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

conn = psycopg2.connect(
    f"host=db dbname={os.environ['POSTGRES_DB']} password={os.environ['POSTGRES_PASSWORD']} user=postgres")

updater = Updater(
    token=os.environ['BOT_TOKEN'], use_context=True)

dispatcher = updater.dispatcher

for module in handlers.__all__:
    dispatcher.add_handler(getattr(handlers, module).handler(conn))

updater.start_polling()
