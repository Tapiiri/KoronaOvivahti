from telegram.ext import CommandHandler
from botlib.dbhelpers import list_my_spaces
import datetime
from psycopg2 import ProgrammingError

def myspaces(update, context):
    pool = context.bot_data["pool"]
    tg_id = update.effective_user.id
    fields = ["title", "handle", "date"]
    with pool.getconn() as conn:
        records = list_my_spaces(conn, fields, tg_id).fetchall()
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(records))
    


handler = CommandHandler('myspaces', myspaces)
