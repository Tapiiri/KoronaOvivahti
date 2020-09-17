from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Filters
from botlib.dbhelpers import list_my_spaces, get_user_id, update_space
import datetime
from psycopg2 import ProgrammingError
from . import cancel
from . import newspace
from ._with_conn_dec import with_conn

@with_conn
def myspaces(update, context, conn):
    tg_id = update.effective_user.id
    fields = ["handle", "title", "date", "id"]
    spaces = list_my_spaces(conn, fields, tg_id).fetchall()
    message = "Choose a space."
    context.user_data["spaces"] = {}
    for space in spaces:
        context.user_data["spaces"][space[0]] = {
            "title": space[1], 
            "date": space[2],
            "id": space[3]}
        message += "\n/{}, {} {}".format(
            space[0],
            space[1],
            space[2].strftime("%a %d.%m.%Y")
        )
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message)
    return "choose_space"

def choose_space(update, context):
    space_handles = context.user_data["spaces"].keys()
    chosen_handle = update.message.text
    if "/" in chosen_handle:
        chosen_handle = update.message.text[1:]
    if chosen_handle in space_handles:
        space = {
            **context.user_data["spaces"][chosen_handle],
            "handle":chosen_handle
        }
        context.user_data["editedspace"] = space
        message = "/edit space, or /cancel\nName: {title}\nHandle: {handle}\nDate: {date}".format(
                        **{
                            **space,
                            "date": space["date"].strftime("%a %d.%m.%Y")
                        }
                    )
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message)
        return "edit_space"
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Incorrect handle")
        return generateqr(update, context)

def edit_space(update, context):
    context.user_data["newspace"] = context.user_data["editedspace"]
    return newspace.confirm(update, context)

@with_conn
def update_the_space(update, context, conn):
    space = context.user_data["newspace"]
    success = update_space(conn, space)
    if success:
        context.bot.send_message(
                chat_id=update.effective_chat.id, text="Space updated!")
        return "END"
    else: 
        context.bot.send_message(
                chat_id=update.effective_chat.id, text="Failed to update...try again or /cancel")
        return newspace.confirm(update, context)
                

   


handler = ConversationHandler(
    [CommandHandler('myspaces', myspaces)],
    {
        "choose_space": [cancel.handler, MessageHandler(Filters.text, choose_space)],
        "edit_space": [cancel.handler, ConversationHandler(
            [CommandHandler('edit', edit_space)],
            {
                **newspace.handler.states,
                "confirm_or_edit": [
                    *newspace.handler.states["confirm_or_edit"][:-1],
                    CommandHandler("confirm", update_the_space)
                ]
            },
            [],
            map_to_parent = {"END":ConversationHandler.END}
        )],
    },
    []
    )
