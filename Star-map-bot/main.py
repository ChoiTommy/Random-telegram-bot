
import logging, os, asyncio # , requests

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pyppeteer import launch # https://github.com/pyppeteer/pyppeteer
# from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from datetime import *
from pathlib import Path
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO
)

logger = logging.getLogger(__name__)

# Load credentials from enviroment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Coordinates of Singapore 1.3521° N, 103.8198° E

# async def get_image():
#     ahora = datetime.now(timezone(timedelta(hours = 8)))
#     url = f'https://in-the-sky.org/skymap2.php?no_cookie=1&latitude=1.3521&longitude=103.8198&timezone=+8.00&year={ahora.year}&month={ahora.month}&day={ahora.day}&hour={ahora.hour}&min={ahora.second}'
#     browser = await launch()
#     page = await browser.newPage()
#     await page.goto(url)
#     await page.screenshot(
#         path = 'map.png',
#         clip = dict(
#             x = 0,
#             y = 600,
#             width = 800,
#             height = 715
#         ))
#     await browser.close()


# asyncio.get_event_loop().run_until_complete(get_image())

def start(update: Update, context: CallbackContext) -> None:

    update.message.reply_photo(photo = open('map.png', 'rb'))

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register a command handler
    dispatcher.add_handler(CommandHandler('start', start))

    # Start the Bot using polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
