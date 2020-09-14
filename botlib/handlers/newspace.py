from telegram.ext import CommandHandler, ConversationHandler
from functools import partial
from dbhelpers import set_space, list_spaces
import datetime
from psycopg2 import ProgrammingError

def newspace(pool=None, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(records))

def ask_title(pool=None, update, context):

def ask_handle(pool, update, context):

def ask_date(pool=None, update, context):



    


def handler(pool): return ConversationHandler(
    [CommandHandler('newspace', partial(newspace, pool))],
    {            
        "title": "Smökki",
        "handle": "smokki",
        "date":
    },
    [],
    allowreenty=True)
