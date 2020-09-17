from telegram.ext import CommandHandler
from telegram.ext.filters import Filters
from botlib.dbhelpers import upsert_user
from .join import join

def start_with_payload(update, context):
    pool = context.bot_data["pool"]
    with pool.getconn() as conn:
        greeting = "Hi, and welcome to KoronaOvivahti!"
        user = {
            "tg_id": update.effective_user.id,
            "handle": update.effective_user.name,
            "name": update.effective_user.full_name
        }
        upsert_user(conn, user)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=str(greeting))
        try:
            payload = context.args[0]
        except IndexError:
            try:
                payload = update.message.text.split(" ")[1]
            except IndexError:
                return
    return join(update, context)




handler = CommandHandler("start", start_with_payload)
