from telegram.ext import CommandHandler
from functools import partial


def start(conn, update, context):
    greeting = "Hi, and welcome to KoronaOvivahti!"
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    records = cur.fetchall()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=str(records))


def handler(conn): return CommandHandler('start', partial(start, conn))
