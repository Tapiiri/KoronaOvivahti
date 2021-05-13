from telegram.ext import CommandHandler
from botlib.dbhelpers import upsert_user
from telegram.ext.filters import Filters
from ._with_conn_dec import with_conn


@with_conn
def start(update, context, conn):
    greeting = "Hi, and welcome to KoronaOvivahti!"
    user = {
        "tg_id": update.effective_user.id,
        "handle": update.effective_user.name,
        "name": update.effective_user.full_name
    }
    upsert_user(conn, user)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=greeting)


handler = CommandHandler('start', start)
