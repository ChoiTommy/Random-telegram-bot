'''
 Reference
 https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples
 https://python-telegram-bot.readthedocs.io/en/stable/index.html
'''
import logging

from telegram import Update, ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(update.message.chat.id, 'You look a bit confused man. Is that because of the painful engineering assignment? Try me if you face any difficulty in your engineering courses!')
    context.bot.send_message(
        update.message.chat.id,
        'Did your stuff move?',
        reply_markup = ReplyKeyboardMarkup([['Yes', 'No']], resize_keyboard = True)
    )
    return 0

def should_it_move(update: Update, context: CallbackContext) -> int: # state 0
    text = update.message.text
    context.user_data['DID_IT_MOVE'] = True if text == 'Yes' else False
    context.bot.send_message(
        update.message.chat.id,
        'Should it?',
        reply_markup = ReplyKeyboardMarkup([['Yes', 'No']], resize_keyboard = True)
    )
    return 1

def solution(update: Update, context: CallbackContext) -> int: # state 1
    text = update.message.text
    context.user_data['SHOULD_IT_MOVE'] = True if text == 'Yes' else False

    if context.user_data['DID_IT_MOVE'] != context.user_data['SHOULD_IT_MOVE']:
        if context.user_data['DID_IT_MOVE']:
            context.bot.send_photo(update.message.chat.id, 'https://imgur.com/t/duct_tape/DcB488r', 'Here\'s your tape. Problem solved. Close file.', reply_markup=ReplyKeyboardRemove())
        else:
            context.bot.send_photo(update.message.chat.id, 'https://imgur.com/gallery/5ByolFl', 'Go and grab the cologne loved by most engineers - WD-40. Trust me it WORKS.', reply_markup=ReplyKeyboardRemove())
    else:
        context.bot.send_message(update.message.chat.id, 'Fret not! Your stuff is fine.', reply_markup=ReplyKeyboardRemove())

    context.user_data.clear()
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(update.message.chat.id, 'The process is cancelled. Type the command /start again to restart the program.', reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END

def get_token() -> str:
    f = open('key.txt', 'r')
    key = f.readline()
    f.close()
    return key

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(get_token())

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