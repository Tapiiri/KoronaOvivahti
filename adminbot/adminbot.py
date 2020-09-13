import os
from telegram.ext import Updater
import logging

import handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(
    token=os.environ['ADMINBOT_TOKEN'], use_context=True)

dispatcher = updater.dispatcher

for module in handlers.__all__:
    dispatcher.add_handler(getattr(handlers, module).handler)

updater.start_polling()
