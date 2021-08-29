# https://www.epochconverter.com/

# TODO custom location, pdf to image, red scale img, auto detect timezone of users, star map features toggles, etc.
import logging
import os
import time


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
# from pyppeteer import launch # https://github.com/pyppeteer/pyppeteer
# from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# from datetime import *
# from pathlib import Path
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO
)

logger = logging.getLogger(__name__)

# Load credentials from enviroment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
SG_LAT = 1.3521 # Coordinates of Singapore 1.3521° N, 103.8198° E
SG_LONG = 103.8198
STAR_MAP_URL = f'https://www.heavens-above.com/SkyAndTelescope/StSkyChartPDF.ashx?time=%t&latitude={SG_LAT}&longitude={SG_LONG}&location=Singapore&utcOffset=28800000&showEquator=false&showEcliptic=true&showStarNames=true&showPlanetNames=true&showConsNames=true&showConsLines=true&showConsBoundaries=false&showSpecials=false&use24hClock=true'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Stargazing bot')

def send_star_map(update: Update, context: CallbackContext) -> None:
    update.message.reply_document(
        document = STAR_MAP_URL.replace('%t', str(int(time.time()*1000)))
    )
    update.message.reply_text('Enjoy the stunning stars! Be considerate and leave no trace while stargazing!')

def credits(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text = 'Star map is made available to you by skyandtelescope.org. This bot is not affiliated with skyandtelescope.org. Visit their website for more infomation.',
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Visit skyandtelescope.org", url='https://skyandtelescope.org/')],
            [InlineKeyboardButton("Check out their interactive sky chart", url='https://skyandtelescope.org/interactive-sky-chart/')]
        ])
    )

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register a command handler
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('starmap', send_star_map))
    dispatcher.add_handler(CommandHandler('credits', credits))

    # Start the Bot using polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()