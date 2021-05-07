import random
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, CallbackContext, CallbackQueryHandler

UP, DOWN, LEFT, RIGHT = '500', '501', '502', '503'
MOVEMENT = [UP, DOWN, LEFT, RIGHT]
init_game_board_keyboard = [
    [InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1')],
    [InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1')],
    [InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1')],
    [InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1'), InlineKeyboardButton("0", callback_data = '-1')],
    [InlineKeyboardButton("^", callback_data = UP)],
    [InlineKeyboardButton("<", callback_data = LEFT), InlineKeyboardButton(">", callback_data = RIGHT)],
    [InlineKeyboardButton("v", callback_data = DOWN)]
]

init_game_board_data = [ # [0..3][0..3]
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

random.seed(10)


def new_game_board(update: Update, context: CallbackContext) -> None:
    pos1 = random.randint(0, 15)
    pos2 = random.randint(0, 15)
    while pos2 == pos1:
        pos2 = random.randint(0, 15)

    board = init_game_board_keyboard
    board_data = init_game_board_data
    print(board_data)

    board_data[pos1 // 4][pos1 % 4] = 2*(random.randint(1, 2))
    board_data[pos2 // 4][pos2 % 4] = 2*(random.randint(1, 2))

    board[pos1 // 4][pos1 % 4].text = str(board_data[pos1 // 4][pos1 % 4])
    board[pos2 // 4][pos2 % 4].text = str(board_data[pos2 // 4][pos2 % 4])

    update.message.reply_text(
        '2048',
        reply_markup = InlineKeyboardMarkup(board)
    )
