from telegram.ext import CommandHandler
from botlib.dbhelpers import upsert_user
from telegram.ext.filters import Filters

def start(update, context):
    pool = context.bot_data["pool"]
    with pool.getconn() as conn:
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
