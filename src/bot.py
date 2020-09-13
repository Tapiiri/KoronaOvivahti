from telegram.ext import Updater
import logging

import handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(
    token='1208159439:AAEH0Ruz-5PyVpNGMUUpve1T4DuFCN11Yec', use_context=True)

dispatcher = updater.dispatcher

for module in handlers.__all__:
    dispatcher.add_handler(getattr(handlers, module).handler)

updater.start_polling()
