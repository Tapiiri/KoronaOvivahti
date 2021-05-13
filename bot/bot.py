import os
from functools import partial
import psycopg2.pool
from telegram.ext import Updater
import logging
from botlib.handlers import start, join, leave, start_with_payload
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

pool = psycopg2.pool.ThreadedConnectionPool(0, 10,
                                            f"host={os.environ['POSTGRES_HOST']} \
        dbname={os.environ['POSTGRES_DB']} \
        password={os.environ['POSTGRES_PASSWORD']} \
        user={os.environ['POSTGRES_USER']}")

updater = Updater(
    token=os.environ['BOT_TOKEN'], use_context=True)

dispatcher = updater.dispatcher
dispatcher.bot_data["pool"] = pool

bot_handler_modules = [
    join,
    leave,
    start_with_payload
]

for module in bot_handler_modules:
    dispatcher.add_handler(module.handler)

updater.start_polling()
updater.idle()
