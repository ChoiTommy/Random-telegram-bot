import logging, os, game_2048 as game

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

def inline_buttons(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    query.answer()
    if query.data == '-1':
        return
    elif query.data in game.MOVEMENT:
        query.edit_message_text(query.data)
        query.edit_message_reply_markup(query.message.reply_markup)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handler
    dispatcher.add_handler(CallbackQueryHandler(inline_buttons))
    dispatcher.add_handler(CommandHandler('2048', game.new_game_board))

    # Start the Bot using polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()