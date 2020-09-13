import os

import psycopg2
from telegram.ext import Updater
import logging

import handlers
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

conn = psycopg2.connect(f"dbname={os.environ['POSTGRES_DB']} password={os.environ['POSTGRES_PASSWORD']} user=postgres")
# cur = conn.cursor()
# cur.execute("SELECT * FROM my_data");
# records = cur.fetchall()

updater = Updater(
    token=os.environ['BOT_TOKEN'], use_context=True)

dispatcher = updater.dispatcher

for module in handlers.__all__:
    dispatcher.add_handler(getattr(handlers, module).handler)

updater.start_polling()
