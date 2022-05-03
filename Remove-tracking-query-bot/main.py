'''
https://en.wikipedia.org/wiki/UTM_parameters
https://docs.python.org/3/library/urllib.parse.html
https://stackoverflow.com/questions/38565952/how-to-receive-messages-in-group-chats-using-telegram-bot-api
'''
import logging, os #, urlexpander # TODO https://github.com/SMAPPNYU/urlExpander

from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from urllib.parse import urlparse, parse_qs, urlencode
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

def remove_tracker_or_unshorten(update: Update, context: CallbackContext) -> None:
    for og_url in update.message.parse_entities('url').values():
        modified = False
        parsed_url = urlparse(og_url)
        query_dict = parse_qs(parsed_url.query)
        for key in list(query_dict): # creates a shallow copy of the items of the dictionary
            if 'utm_' in key:
                del query_dict[key]
                modified = True
        new_url = parsed_url._replace(query=urlencode(query_dict, doseq=True))
        if modified: update.message.reply_text(f"From {update.message.from_user.full_name}\n{new_url.geturl()}")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("start")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.entity("url"), remove_tracker_or_unshorten))
    dispatcher.add_handler(CommandHandler('start', start))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()