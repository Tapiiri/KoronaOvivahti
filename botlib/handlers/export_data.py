from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram.utils.helpers import create_deep_linked_url
from botlib.dbhelpers import list_my_spaces, get_user_id, door_event_export
from . import cancel
import datetime
import requests
import logging
import io
import os

def export_data(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Are you sure?\n/export_data\n/cancel")
    return "confirmation"

def choose_space(update, context):
    pool = context.bot_data["pool"]
    tg_id = update.effective_user.id
    fields = ["handle", "title", "date"]
    with pool.getconn() as conn:
        spaces = list_my_spaces(conn, fields, tg_id)
        context.user_data["space_handles"] = []
        message = "Choose space to export user data from."
        for space in spaces:
            context.user_data["space_handles"].append(space[0])
            message += "\n/{}, {} {}".format(
                space[0],
                space[1],
                space[2].strftime("%a %d.%m.%Y")
            )
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message)
    return "choose_space"

def create_db_export(update, context):
        space_handles = context.user_data["space_handles"]
        chosen_handle = update.message.text
        if "/" in chosen_handle:
            chosen_handle = update.message.text[1:]
        if chosen_handle in space_handles:
            pool = context.bot_data["pool"]
            with pool.getconn() as conn:
                tg_id = update.effective_user.id    
                user_id = get_user_id(conn, tg_id).fetchone()[0]
                timestamp = "{:.0f}".format(datetime.datetime.now().timestamp())
                export_path = f"{user_id}_{timestamp}_{chosen_handle}_export.csv"    
                success = door_event_export(conn, chosen_handle, export_path)
                if success:
                    f = open("/tmp/db_exports/{}".format(export_path), 'rb')
                    context.bot.send_document(
                        chat_id=update.effective_chat.id, 
                        document=f)
                return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Incorrect handle")
            return choose_space(update, context)
    

handler = ConversationHandler(
    [CommandHandler('export_data', export_data)],
    {
        "confirmation": [cancel.handler, MessageHandler(Filters.text, choose_space)],
        "choose_space": [cancel.handler, MessageHandler(Filters.text, create_db_export)]
    },
    []
)
