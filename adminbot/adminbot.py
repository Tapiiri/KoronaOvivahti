import os
from functools import partial
import psycopg2.pool
from telegram.ext import Updater
import logging

import handlers
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
                    
pool = psycopg2.pool.ThreadedConnectionPool(0, 10,
    f"host={os.environ['POSTGRES_HOST']} \
        dbname={os.environ['POSTGRES_DB']} \
        password={os.environ['POSTGRES_PASSWORD']} \
        user={os.environ['POSTGRES_USER']}")

updater = Updater(
    token=os.environ['ADMINBOT_TOKEN'], use_context=True)

dispatcher = updater.dispatcher

for module in handlers.__all__:
    dispatcher.add_handler(getattr(handlers, module).handler(pool))

updater.start_polling()
