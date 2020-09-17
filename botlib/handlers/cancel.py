from telegram.ext import MessageHandler, ConversationHandler
from telegram.ext.filters import Filters
import re


def cancel(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Stopping")
    return ConversationHandler.END

pattern = re.compile("cancel|stop|abort")
handler = MessageHandler(Filters.regex(pattern), cancel)
