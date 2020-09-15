from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from functools import partial
from dbhelpers import set_space, list_spaces
import datetime
import logging
from psycopg2 import ProgrammingError, InternalError, OperationalError

def newspace(update, context):
    context.user_data["newspace"] = {}
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Name of space")
    return "title"

def set_title(update, context):
    title = update.message.text
    context.user_data["newspace"] = {**context.user_data["newspace"], "title":title}
    return ask_handle(update, context)

def ask_handle(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Handle of space")
    return "handle"

def set_handle(pool, update, context):
    handle = update.message.text
    with pool.getconn() as conn:
        spaces_with_same_handle = list_spaces(conn, fields=["handle"], params={"handle":handle})
        try:
            spaces_with_same_handle.fetchone()
            context.user_data["newspace"] = {**context.user_data["newspace"], "handle":handle}
            return ask_date(update, context)
        except ProgrammingError:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Handle in use")
            return ask_handle(update, context)

def ask_date(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Date of space, format DD MM YYYY")
    return "date"

def set_date(pool, update, context):
    date_text = update.message.text
    try:
        date_delimiter = date_text[2]   
        date_list = date_text.split(date_delimiter)
        year = int(date_list[2])
        month = int(date_list[1])
        day = int(date_list[0])
        date = datetime.date(year, month, day)
        context.user_data["newspace"] = {**context.user_data["newspace"], "date":date}
        return create_space(pool, update, context)
    except (IndexError, TypeError):
        logging.exception("Date didn't work out")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Give correct date")
        return ask_date(update, context)

def create_space(pool, update, context):
    space = context.user_data["newspace"]
    space["owner_id"] = update.effective_user.id
    try:
        with pool.getconn() as conn:
                set_space(conn, space)
    except (ProgrammingError,  InternalError, OperationalError):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Something went wrong - try again later")
        logging.exception("Something went wrong when a user was setting a new space")
    context.bot.send_message(
            chat_id=update.effective_chat.id, text="Space created!")
    return ConversationHandler.END

def fallback(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ok...? I'll end this here.")
        return ConversationHandler.END


    


def handler(pool): return ConversationHandler(
    [CommandHandler('newspace', newspace)],
    {            
        "title": [MessageHandler(Filters.text, set_title)],
        "handle": [MessageHandler(Filters.text, partial(set_handle, pool))],
        "date": [MessageHandler(Filters.text, partial(set_date, pool))],
    },
    [
        MessageHandler(Filters.text, fallback)
    ],
    allow_reentry=True)
