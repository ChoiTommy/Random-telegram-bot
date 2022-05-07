# https://www.epochconverter.com/
# https://nominatim.org/release-docs/develop/api/Reverse/

# TODO pdf to image, red scale img, timezone support, star map features toggles, etc.
import logging
import os
import time
import json
import urllib.request, ssl

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from dotenv import load_dotenv
# from geopy.geocoders import Nominatim


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO
)
logger = logging.getLogger(__name__)

# Load credentials from enviroment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# starmap URLs
STARMAP_URL = "https://www.heavens-above.com/SkyAndTelescope/StSkyChartPDF.ashx"
'''params: time, latitude, longitude, location'''
REST_OF_THE_URL = f"utcOffset=28800000&showEquator=false&showEcliptic=true&showStarNames=true&showPlanetNames=true&showConsNames=true&showConsLines=true&showConsBoundaries=false&showSpecials=false&use24hClock=true"



def send_star_map(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)
    with open("locations.json", 'r') as file:
        data = json.load(file)

    if data.get(user_id) != None: # check_if_user_data_exists(update.effective_user):

        lat = str(data[user_id]["latitude"])
        longi = str(data[user_id]["longitude"])
        address = data[user_id]["address"].replace(',', "%2c").replace(' ', "%20")

        fetch_target = f"{STARMAP_URL}?time={str(int(time.time()*1000))}&latitude={lat}&longitude={longi}&location={address}&{REST_OF_THE_URL}"

        update.message.reply_document(document = fetch_target)
        update.message.reply_text("Enjoy the stunning stars\! Be considerate and *leave no trace* while stargazing\!", parse_mode=ParseMode.MARKDOWN_V2)
    else:
        update.message.reply_text("Please set your location with /setlocation first!")


def show_user_info(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)
    with open("locations.json", 'r') as file:
        data = json.load(file)

    if data.get(str(update.effective_user.id)) != None: # check_if_user_data_exists(update.effective_user):
        update.message.reply_text(
            f'''Hi @{update.effective_user.username},
Your currently set location is
Latitude: {data[user_id]["latitude"]}
Longitude: {data[user_id]["longitude"]}
Location: {data[user_id]["address"]}
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
        text = "Star map is made available to you by skyandtelescope.org. This bot is not affiliated with skyandtelescope.org. Visit their website for more information.",
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Visit skyandtelescope.org", url="https://skyandtelescope.org/")],
            [InlineKeyboardButton("Check out their interactive sky chart", url="https://skyandtelescope.org/interactive-sky-chart/")]
        ])
    )


def set_location(update: Update, context: CallbackContext) -> int:
    user_id = str(update.effective_user.id)
    with open("locations.json", 'r') as file:
        data = json.load(file)
    context.user_data["JSON"] = data

    if data.get(user_id) != None: # check_if_user_data_exists(update.effective_user):
        update.message.reply_text(f"Your current location is {data[user_id]['latitude']}, {data[user_id]['longitude']} ({data[user_id]['address']}).")
        update.message.reply_text("Send your new location if you wish to change. /cancel to keep the current setting.")
    else:
        update.message.reply_text("Send your location to me :O Trust me I won\'t tell others ~\(unless someone pays me A LOT\)~ ", parse_mode = ParseMode.MARKDOWN_V2)
    return 0

def update_location(update: Update, context: CallbackContext) -> int:
    user_id = str(update.effective_user.id)
    lat = update.message.location.latitude
    longi = update.message.location.longitude
    data = context.user_data["JSON"]

    context = ssl._create_unverified_context()
    NOMINATIM_REVERSE_API = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={longi}"
    # print(NOMINATIM_REVERSE_API)
    with urllib.request.urlopen(NOMINATIM_REVERSE_API, context=context) as address_file:
        address_data = json.load(address_file)

    address_string = f"{address_data['address']['suburb']}, {address_data['address']['country']}"

    if data.get(user_id) == None:
        data.update({user_id:{"username": update.effective_user.username, "latitude": lat, "longitude" : longi, "address" : address_string}})
    else:
        data[user_id]["latitude"] = lat
        data[user_id]["longitude"] = longi
        data[user_id]["address"] = address_string

    with open("locations.json", 'w') as file:
        json.dump(data, file, indent = 4)
    update.message.reply_text(f"All set! Your new location is {lat}, {longi} ({address_string}).")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('ℹ️The setup process is cancelled.')
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