from telegram.ext import CommandHandler


def start(update, context):
    greeting = "Hi! Use me to register in and out for an event!"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=greeting)


handler = CommandHandler('start', start)
