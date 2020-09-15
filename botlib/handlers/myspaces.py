from telegram.ext import CommandHandler
from functools import partial
from dbhelpers import list_spaces
import datetime
from psycopg2 import ProgrammingError

def myspaces(update, context):
    pool = context.bot_data["pool"]
    with pool.getconn() as conn:
        records = list_spaces(conn).fetchall()
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(records))
    


handler = CommandHandler('myspaces', myspaces)
