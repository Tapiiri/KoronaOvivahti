from telegram.ext import MessageHandler


def unknown(update, context):
    greeting = "Hi, and welcome to KoronaOvivahti!"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=greeting)


handler = MessageHandler('start', unknown)
