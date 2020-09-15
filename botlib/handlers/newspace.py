from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from functools import partial
from dbhelpers import set_space, list_spaces
import datetime
import logging
from psycopg2 import ProgrammingError, InternalError, OperationalError
from psycopg2.errors import UniqueViolation

def newspace(update, context):
    context.user_data["newspace"] = {}
    return ask_title(update, context)

def ask_title(update, context):
    try: 
        title = context.user_data["newspace"]["title"]
        if title:
            return set_title(update, context, existing_title=title)
    except KeyError:
        pass
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Name of space")
    return "title"

def set_title(update, context, existing_title=None):
    title = existing_title or update.message.text
    context.user_data["newspace"] = {**context.user_data["newspace"], "title":title}
    return ask_handle(update, context)

def ask_handle(update, context):
    try: 
        handle = context.user_data["newspace"]["handle"]
        if handle:
            return set_handle(update, context, existing_handle=handle)
    except KeyError:
        pass
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Handle of space")
    return "handle"

def set_handle(update, context, existing_handle=None):
    handle = existing_handle or update.message.text
    handle = handle.lower()
    pool = context.bot_data["pool"]
    with pool.getconn() as conn:
        spaces_with_same_handle = list_spaces(conn, fields=["handle"], params={"handle":handle})
        if spaces_with_same_handle.fetchone() is None:
            context.user_data["newspace"] = {**context.user_data["newspace"], "handle":handle}
            return ask_date(update, context)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Handle already in use")
            return ask_handle(update, context)

def ask_date(update, context):
    try: 
        date = context.user_data["newspace"]["date"]
        if date:
            date_text = date.strftime("%d.%m.%Y")
            return set_date(update, context, existing_date_text=date_text)
    except KeyError:
        pass
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Date of space, format DD MM YYYY")
    return "date"

def set_date(update, context, existing_date_text=None):
    date_text = existing_date_text or update.message.text
    try:
        date_delimiter = date_text[2]   
        date_list = date_text.split(date_delimiter)
        year = int(date_list[2])
        month = int(date_list[1])
        day = int(date_list[0])
        date = datetime.date(year, month, day)
        context.user_data["newspace"] = {**context.user_data["newspace"], "date":date}
        return confirm(update, context)
    except (IndexError, TypeError, ValueError):
        logging.exception("Date didn't work out")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Give correct date")
        return ask_date(update, context)

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
                        "date": space["date"].strftime("%d.%m.%Y")
                    }))
    return "confirm_or_edit"

    return confirm

def ask_again(value, callback):
    def again_wrapper(update, context):
        context.user_data["newspace"][value] = None
        return callback(update, context)

    return again_wrapper

def create_space(update, context):
    space = context.user_data["newspace"]
    space["owner_id"] = update.effective_user.id
    try:
        pool = context.bot_data["pool"]
        with pool.getconn() as conn:
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
            chat_id=update.effective_chat.id, text="Ok...? I'll end this here.")
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
