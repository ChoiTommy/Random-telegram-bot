# https://www.epochconverter.com/

# TODO custom location, pdf to image, red scale img, auto detect timezone of users, star map features toggles, etc.
import logging
import os
import time
# import json


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
# from pyppeteer import launch # https://github.com/pyppeteer/pyppeteer
# from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# from datetime import *
# from pathlib import Path
from dotenv import load_dotenv
# from geopy.geocoders import Nominatim

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO
)
logger = logging.getLogger(__name__)

# Load credentials from enviroment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
# geolocator = Nominatim(user_agent="Star-map-bot")

# Placeholders: %t (time), %lat (latitude), %long (longitude), %loca (location text)
STAR_MAP_URL = f'https://www.heavens-above.com/SkyAndTelescope/StSkyChartPDF.ashx?time=%t&latitude=%lat&longitude=%long&location=%loca&utcOffset=28800000&showEquator=false&showEcliptic=true&showStarNames=true&showPlanetNames=true&showConsNames=true&showConsLines=true&showConsBoundaries=false&showSpecials=false&use24hClock=true'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Simply send me your location👀\nI\'ll send you a *STAR MAP* in return :\)', parse_mode = ParseMode.MARKDOWN_V2)

def send_star_map(update: Update, context: CallbackContext) -> None:
    lat = update.message.location.latitude
    longi = update.message.location.longitude

    # location = geolocator.reverse((lat, longi))

    fetch_target = STAR_MAP_URL
    fetch_target = fetch_target.replace("%lat", str(lat)).replace("%long", str(longi)).replace('%t', str(int(time.time()*1000))).replace("%loca", ":%29")

    update.message.reply_document(
        document = fetch_target
    )
    update.message.reply_text('Enjoy the stunning stars! Be considerate and leave no trace while stargazing!')

def credits(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text = 'Star map is made available to you by skyandtelescope.org. This bot is not affiliated with skyandtelescope.org. Visit their website for more information.',
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Visit skyandtelescope.org", url='https://skyandtelescope.org/')],
            [InlineKeyboardButton("Check out their interactive sky chart", url='https://skyandtelescope.org/interactive-sky-chart/')]
        ])
    )

# def check_if_user_data_exists(user: User) -> bool, str:
#     loc_file = open('locations.json', 'rt')  #https://realpython.com/python-json/
#     whole = loc_file.read()
#     all_data = json.loads(whole)
#     loc_file.close()
#     if whole.count(str(user.id)) != 0:
#         location = all_data[user.id]
#         return True, location
#     return False, ''


# def ask_for_location(update: Update, context: CallbackContext) -> None:
#     loc_file = open('locations.txt', 'r+')

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register a command handler
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('credits', credits))

    dispatcher.add_handler(MessageHandler(Filters.location, send_star_map))

    # dispatcher.add_handler(ConversationHandler(
    #     entry_points = [],
    #     states = {},
    #     fallbacks =[],
    #     conversation_timeout = 120 # 2 mins
    # ))

    # Start the Bot using polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()