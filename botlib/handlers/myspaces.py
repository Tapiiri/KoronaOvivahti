from telegram.ext import CommandHandler
from botlib.dbhelpers import list_my_spaces
import datetime
from psycopg2 import ProgrammingError
from ._with_conn_dec import with_conn

@with_conn
def myspaces(update, context, conn):
    tg_id = update.effective_user.id
    fields = ["title", "handle", "date"]
    records = list_my_spaces(conn, fields, tg_id).fetchall()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=str(records))
    


handler = CommandHandler('myspaces', myspaces)
