from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Filters
from telegram.utils.helpers import create_deep_linked_url
from dbhelpers import list_my_spaces
from handlers import cancel
import datetime
import requests
import logging
import io
import os

def generateqr(update, context):
    pool = context.bot_data["pool"]
    tg_id = update.effective_user.id
    fields = ["handle", "title", "date"]
    with pool.getconn() as conn:
        spaces = list_my_spaces(conn, fields, tg_id)
        context.user_data["space_handles"] = []
        message = "Choose space for which to generate QR"
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

def check_space(update, context):
    space_handles = context.user_data["space_handles"]
    chosen_handle = update.message.text
    if "/" in chosen_handle:
        chosen_handle = update.message.text[1:]
    if chosen_handle in space_handles:
        qr_payload = create_deep_linked_url(os.environ["USER_BOT_NAME"], chosen_handle)
        qr_request_url = "http://qr:8080/?data={}".format(qr_payload)
        r = requests.get(qr_request_url)
        if r.status_code == 200:
            photo = io.BytesIO(r.content)
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=io.BufferedReader(photo))
        return ConversationHandler.END
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Incorrect handle")
        return generateqr(update, context)
    

handler = ConversationHandler(
    [CommandHandler('generateqr', generateqr)],
    {"choose_space": [cancel.handler, MessageHandler(Filters.text, check_space)]},
    []
)
