from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from functools import partial
from dbhelpers import set_space, list_spaces, get_user_id
import datetime
import logging
from psycopg2 import ProgrammingError, InternalError, OperationalError
from psycopg2.errors import UniqueViolation
import re

def check_value(value_name, context):
    try: 
        value = context.user_data["newspace"][value_name]
        return value
    except KeyError:
        return None

def set_value(value_name, value, context):
    context.user_data["newspace"] = {
            **context.user_data["newspace"],
            value_name : value
        }


def newspace(update, context):
    context.user_data["newspace"] = {}
    return ask_title(update, context)

def ask_title(update, context):
    title =  check_value("title", context)
    if title:
        return set_title(update, context, title)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Name of space")
    return "title"

def set_title(update, context, existing_title=None):
    title = existing_title or update.message.text
    set_value("title", title, context)
    return ask_handle(update, context)

def ask_handle(update, context):
    handle = check_value("handle", context)
    if handle:
        return set_handle(update, context, handle)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Handle of space")
    return "handle"

def handle_available(handle, context):
    pool = context.bot_data["pool"]
    with pool.getconn() as conn:
        spaces_with_same_handle = list_spaces(conn, fields=["handle"], params={"handle":handle})
        return spaces_with_same_handle.fetchone() is None


def set_handle(update, context, existing_handle=None):
    handle = existing_handle or update.message.text
    handle = handle.lower()
    if handle_available(handle, context):
        set_value("handle", handle, context)
        return ask_date(update, context)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Handle already in use")
        return ask_handle(update, context)

def ask_date(update, context):
    date =  check_value("date", context)
    if date:
        date_text = date.strftime("%d.%m.%Y")
        return set_date(update, context, date_text)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Date of space, format DD MM YYYY")
    return "date"

def find_date_delimiter(date_text):
    pattern = re.compile("\D")
    matches = re.finditer(pattern, date_text)
    first_match_index = next(matches).start()
    return date_text[first_match_index]

def parse_date(date_text):
    dl = date_delimiter = find_date_delimiter(date_text)
    date_format = f"%d{dl}%m{dl}%Y"
    date = datetime.datetime.strptime(date_text, date_format).date()
    return date

def set_date(update, context, existing_date_text=None):
    date_text = existing_date_text or update.message.text
    try:
        date = parse_date(date_text)
    except (StopIteration, ValueError):
        logging.exception("Date didn't work out")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Give correct date")
        return ask_date(update, context)
    set_value("date", date, context)
    return confirm(update, context)

def confirm(update, context):
    space = context.user_data["newspace"]
    context.bot.send_message(
            chat_id=update.effective_chat.id, text="""
                /Confirm space? Click value to edit\n
                /Name: {title}
                /Handle: {handle}
                /Date: {date}
                """.format(
                    **{
                        **space,
                        "date": space["date"].strftime("%a %d.%m.%Y")
                    }))
    return "confirm_or_edit"

def ask_again(value, callback):
    def again_wrapper(update, context):
        context.user_data["newspace"][value] = None
        return callback(update, context)

    return again_wrapper

def create_space(update, context):
    pool = context.bot_data["pool"]
    space = context.user_data["newspace"]
    try:
        with pool.getconn() as conn:
            tg_id = update.effective_user.id
            user_id = get_user_id(conn, tg_id).fetchone()
            space["owner_id"] = user_id
            try:
                set_space(conn, space)
            except UniqueViolation:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Handle already in use")
                return ask_again("handle", ask_handle)(update, context)
    except (ProgrammingError,  InternalError, OperationalError):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Something went wrong - try again later")
        logging.exception("Something went wrong when a user was setting a new space")
    context.bot.send_message(
            chat_id=update.effective_chat.id, text="Space created!")
    return ConversationHandler.END

def fallback(update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Ok...? I think I lost track. I'll end this discussion here.")
        return ConversationHandler.END


    


handler = ConversationHandler(
    [CommandHandler('newspace', newspace)],
    {            
        "title": [MessageHandler(Filters.text, set_title)],
        "handle": [MessageHandler(Filters.text, set_handle)],
        "date": [MessageHandler(Filters.text, set_date)],
        "confirm_or_edit": [
                        CommandHandler("name", ask_again("title", ask_title)),
                        CommandHandler("handle",  ask_again("handle", ask_handle)),
                        CommandHandler("date",  ask_again("date", ask_date)),
                        CommandHandler("confirm", create_space)]
    },
    [
        MessageHandler(Filters.text, fallback)
    ],
    allow_reentry=True)
