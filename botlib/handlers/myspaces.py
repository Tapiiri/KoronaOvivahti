from telegram.ext import CommandHandler
from functools import partial
from dbhelpers import list_spaces
import datetime
from psycopg2 import ProgrammingError

def myspaces(pool, update, context):
    with pool.getconn() as conn:
        try:
            records = list_spaces(conn).fetchall()
        except ProgrammingError:
            records = []
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(records))
    


def handler(pool): return CommandHandler('myspaces', partial(myspaces, pool))
