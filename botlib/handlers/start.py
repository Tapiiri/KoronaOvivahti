from telegram.ext import CommandHandler
from functools import partial
from dbhelpers import set_user

def start(pool, update, context):
    with pool.getconn() as conn:
        greeting = "Hi, and welcome to KoronaOvivahti!"
        user = {
            "handle": "tapiiri",
            "name": "Ilmari"
        }
        set_user(conn, user)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(user))

def handler(pool): return CommandHandler('start', partial(start, pool))
