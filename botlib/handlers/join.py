from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Filters
from dbhelpers import list_spaces, join_space
from handlers import cancel

def join(update, context):
    try:
        deep_linked_space = context.args[0]
        return join_space(update, context, deep_linked_space)
    except IndexError:
        return ask_space(update, context)

def ask_space(update, context):
    context.bot.send_message(
            chat_id=update.effective_chat.id, text="What space do you want to join?")
    return "ask_space"

def join_to_space(update, context, deep_linked_space=None):
    space_handle = deep_linked_space or update.message.text
    space_handle = space_handle.lower()
    pool = context.bot_data["pool"]
    with pool.getconn() as conn:
        space = list_spaces(conn, ["id", "title"], {"handle": space_handle}).fetchone()
        if space is not None:
            space_id = space[0]
            tg_id = update.effective_user.id
            join_space(conn, space_id, tg_id)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Space not found - try again")        
            return "ask_space"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Space {} joined!".format(space[1]))
    return ConversationHandler.END

handler = ConversationHandler(
    [CommandHandler('join', join)],
    { "ask_space": [cancel.handler,  MessageHandler(Filters.text, join_to_space)]},
    []
)
