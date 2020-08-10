from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

from .loger import log_error


# BUTTONS -----------------------------------------------------
button_help = 'Help'
button_1 = '1'
button_2_1 = 'Current'
button_2_2 = 'Forecast'
button_3_1 = 'Back'

# KEYBOARDS ---------------------------------------------------
KB_START = [
    [
        KeyboardButton(text=button_help),
        KeyboardButton(text=button_1)
    ],
]

KB_WEATHER = [
    [
        KeyboardButton(text=button_2_1),
        KeyboardButton(text=button_2_2)
    ],
    [
        KeyboardButton(text=button_3_1)
    ],
]

# MARKUPS -----------------------------------------------------
MRK_START = ReplyKeyboardMarkup(
    keyboard=KB_START,
    resize_keyboard=True,
)
MRK_WEATHER = ReplyKeyboardMarkup(
    keyboard=KB_WEATHER,
    resize_keyboard=True,
)


# HANDLERS ----------------------------------------------------
def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Welcome to the bot.",
        reply_markup=MRK_START
    )


def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Help message.",
        reply_markup=MRK_START
    )


def other_message_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Some message.",
        reply_markup=MRK_START
    )

# MAIN HANDLER ------------------------------------------------
@log_error
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == '/start':
        return start_handler(update, context)
    elif text == button_help:
        return button_help_handler(update, context)
    else:
        return other_message_handler(update, context)



