# https://www.epochconverter.com/

# TODO pdf to image, red scale img, auto detect timezone of users, star map features toggles, etc.
import logging
import os
import time
import json


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
# from pyppeteer import launch # https://github.com/pyppeteer/pyppeteer
# from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
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

# Placeholders: %t (time), %lat (latitude), %long (longitude), %loca (location text)
STAR_MAP_URL = f'https://www.heavens-above.com/SkyAndTelescope/StSkyChartPDF.ashx?time=%t&latitude=%lat&longitude=%long&location=%loca&utcOffset=28800000&showEquator=false&showEcliptic=true&showStarNames=true&showPlanetNames=true&showConsNames=true&showConsLines=true&showConsBoundaries=false&showSpecials=false&use24hClock=true'



# commands
def send_star_map(update: Update, context: CallbackContext) -> None:
    with open("locations.json", "r") as file:
        data = json.load(file)

    if data.get(str(update.effective_user.id)) != None: # check_if_user_data_exists(update.effective_user):

        lat = data[str(update.effective_user.id)]["latitude"]
        longi = data[str(update.effective_user.id)]["longitude"]

        fetch_target = STAR_MAP_URL #todo rewrite this
        fetch_target = fetch_target.replace("%lat", str(lat)).replace("%long", str(longi)).replace('%t', str(int(time.time()*1000))).replace("%loca", ":%29")

        update.message.reply_document(
            document = fetch_target
        )
        update.message.reply_text('Enjoy the stunning stars! Be considerate and leave no trace while stargazing!')
    else:
        update.message.reply_text('Please set your location with /setlocation first!')

def show_user_info(update: Update, context: CallbackContext) -> None:
    with open("locations.json", "r") as file:
        data = json.load(file)

    if data.get(str(update.effective_user.id)) != None: # check_if_user_data_exists(update.effective_user):
        update.message.reply_text(
            f'''Hi @{update.effective_user.username},
Your currently set location is
{data[str(update.effective_user.id)]["latitude"]}, {data[str(update.effective_user.id)]["longitude"]}.
/setlocation to modify it.
            '''
        )
    else:
        update.message.reply_text(
            f'''Hi {update.effective_user.username},
You have yet to set any location.
/setlocation to start off.
            '''
        )

def credits(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        text = 'Star map is made available to you by skyandtelescope.org. This bot is not affiliated with skyandtelescope.org. Visit their website for more information.',
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Visit skyandtelescope.org", url='https://skyandtelescope.org/')],
            [InlineKeyboardButton("Check out their interactive sky chart", url='https://skyandtelescope.org/interactive-sky-chart/')]
        ])
    )


def set_location(update: Update, context: CallbackContext) -> int:
    with open("locations.json", "r") as file:
        data = json.load(file)
    context.user_data["JSON"] = data

    if data.get(str(update.effective_user.id)) != None: # check_if_user_data_exists(update.effective_user):
        update.message.reply_text(f'Your current location is {data[str(update.effective_user.id)]["latitude"]}, {data[str(update.effective_user.id)]["longitude"]}.')
        update.message.reply_text('Send your new location if you wish to change. /cancel to keep the current setting.')
    else:
        update.message.reply_text('Send your location to me :O Trust me I won\'t tell others (unless someone pays me A LOT) ')
    return 0

def update_location(update: Update, context: CallbackContext) -> int:
    lat = update.message.location.latitude
    longi = update.message.location.longitude
    data = context.user_data["JSON"]

    if data.get(str(update.effective_user.id)) == None:
        data.update({str(update.effective_user.id):{"username": update.effective_user.username, "latitude": lat, "longitude" :longi}})
    else:
        data[str(update.effective_user.id)]["latitude"] = lat
        data[str(update.effective_user.id)]["longitude"] = longi

    with open("locations.json", "w") as file:
        json.dump(data, file, indent = 4)
    update.message.reply_text(f'All set! Your new location is {lat}, {longi}.')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('ℹ️The process is cancelled.')
    return ConversationHandler.END

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register a command handler
    dispatcher.add_handler(CommandHandler('credits', credits))
    dispatcher.add_handler(CommandHandler('starmap', send_star_map))
    dispatcher.add_handler(CommandHandler('myinfo', show_user_info))

    # dispatcher.add_handler(MessageHandler(Filters.location, send_star_map))

    dispatcher.add_handler(ConversationHandler(
        entry_points = [CommandHandler('setlocation', set_location)],
        states = {
            0: [MessageHandler(Filters.location, update_location)]
        },
        fallbacks = [CommandHandler('cancel', cancel)],
        conversation_timeout = 120 # 2 mins
    ))

    # Start the Bot using polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()