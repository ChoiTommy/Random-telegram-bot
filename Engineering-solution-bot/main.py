'''
 References
 https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples
 https://python-telegram-bot.readthedocs.io/en/stable/index.html
'''
import logging, os

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('You look a bit confused man. Is that because of the painful engineering assignment? Try me if you face any difficulty in your engineering courses!')
    update.message.reply_text(
        'Did your stuff move?',
        reply_markup = ReplyKeyboardMarkup([['Yes', 'No']], resize_keyboard = True)
    )
    return 0

def should_it_move(update: Update, context: CallbackContext) -> int: # state 0
    text = update.message.text
    context.user_data['DID_IT_MOVE'] = True if text == 'Yes' else False
    update.message.reply_text(
        'Should it?',
        reply_markup = ReplyKeyboardMarkup([['Yes', 'No']], resize_keyboard = True)
    )
    return 1

def solution(update: Update, context: CallbackContext) -> int: # state 1
    text = update.message.text
    context.user_data['SHOULD_IT_MOVE'] = True if text == 'Yes' else False

    if context.user_data['DID_IT_MOVE'] != context.user_data['SHOULD_IT_MOVE']:
        if context.user_data['DID_IT_MOVE']:
            update.message.reply_photo('https://imgur.com/t/duct_tape/DcB488r', 'Here\'s your tape. Problem solved. Close file.', reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_photo('https://imgur.com/gallery/5ByolFl', 'Go and grab the cologne loved by most engineers - WD-40. Trust me it WORKS.', reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Fret not! Your stuff is fine.', reply_markup=ReplyKeyboardRemove())

    context.user_data.clear()
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('The process is cancelled. Type the command /start again to restart the program.', reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # add conversation handler
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler("start", start)], # list
        states = { # dict
            0: [MessageHandler(Filters.regex('^Yes$') | Filters.regex('^No$'), should_it_move)],
            1: [MessageHandler(Filters.regex('^Yes$') | Filters.regex('^No$'), solution)],
        },
        fallbacks = [MessageHandler(~ Filters.regex('^Yes$') & ~ Filters.regex('^No$'), cancel)],
        #conversation_timeout = 10
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()