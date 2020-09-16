from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Filters
from botlib.dbhelpers import list_spaces, leave_space
from . import cancel

def leave(update, context):
    try:
        deep_linked_space = context.args[0]
        return leave_space(update, context, deep_linked_space)
    except IndexError:
        return ask_space(update, context)

def ask_space(update, context):
    context.bot.send_message(
            chat_id=update.effective_chat.id, text="What space do you want to leave?")
    return "ask_space"

def leave_from_space(update, context, deep_linked_space=None):
    space_handle = deep_linked_space or update.message.text
    space_handle = space_handle.lower()
    pool = context.bot_data["pool"]
    with pool.getconn() as conn:
        space = list_spaces(conn, ["id", "title"], {"handle": space_handle}).fetchone()
        if space is not None:
            space_id = space[0]
            tg_id = update.effective_user.id
            success = leave_space(conn, space_id, tg_id)
            if not success:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text="You've already left {}.".format(space[1]))
                return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Space not found - try again")        
            return "ask_space"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Space {} left!".format(space[1]))
    return ConversationHandler.END

handler = ConversationHandler(
    [CommandHandler('leave', leave)],
    { "ask_space": [cancel.handler, MessageHandler(Filters.text, leave_from_space)]},
    []
)
