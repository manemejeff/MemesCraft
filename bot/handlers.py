from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from api.imgflip import get_memes, craft_meme
from .loger import log_error

# BUTTONS -----------------------------------------------------
button_help = '/help'
btn_start = '/choose_meme'
btn_next_page = '/next_page'
btn_prev_page = '/prev_page'
btn_back = '/back'
btn_home = '/home'

# KEYBOARDS ---------------------------------------------------
KB_START = [
    [
        KeyboardButton(text=button_help),
        KeyboardButton(text=btn_start)
    ],
]

# MARKUPS -----------------------------------------------------
MRK_START = ReplyKeyboardMarkup(
    keyboard=KB_START,
    resize_keyboard=True,
)


# FUNCTIONS ---------------------------------------------------
def create_kb(memes_list, page):

    items = page * 4

    keyboard = [
        [
            KeyboardButton(text=memes_list[items - 4]['name']),
            KeyboardButton(text=memes_list[items - 3]['name']),
        ],
        [
            KeyboardButton(text=memes_list[items - 2]['name']),
            KeyboardButton(text=memes_list[items - 1]['name']),
        ],
        [
            KeyboardButton(text=btn_prev_page),
            KeyboardButton(text=btn_next_page),
        ]
    ]
    return keyboard


# HANDLERS ----------------------------------------------------
def start_handler(update: Update, context: CallbackContext):
    context.user_data['stage'] = 0

    update.message.reply_text(
        text="Welcome to the bot.",
        reply_markup=MRK_START
    )


def button_help_handler(update: Update, context: CallbackContext):
    context.user_data['stage'] = 0

    update.message.reply_text(
        text="Bratishka izvini chto translitom, no mne vpadlu perekluchat/"
             "karoche tut viberaesh mem i pishesh nadpis na nego/"
             "vse legko - glavnoe ne oblazhatsya",
        reply_markup=MRK_START
    )


def choose_meme_handler(update: Update, context: CallbackContext):
    # try:
    memes = get_memes()
    context.user_data['memes_list'] = memes['data']['memes']
    print(context.user_data['page'])
    keyboard = create_kb(context.user_data['memes_list'], context.user_data['page'])

    MRK_MEMES_LIST = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

    update.message.reply_text(
        text="Now choose your meme by the name",
        reply_markup=MRK_MEMES_LIST
    )
    context.user_data['stage'] = 1


# except Exception:
#     update.message.reply_text(
#         text=f"Error {Exception}",
#         reply_markup=MRK_START
#     )


def other_page_handler(update: Update, context: CallbackContext):
    keyboard = create_kb(context.user_data['memes_list'], context.user_data['page'])

    MRK_MEMES_LIST = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

    update.message.reply_text(
        text="Now choose your meme by the name",
        reply_markup=MRK_MEMES_LIST
    )
def get_text0_handler(update: Update, context: CallbackContext):
    pass

def get_text1_handler(update: Update, context: CallbackContext):
    pass

def confirm_meme_handler(update: Update, context: CallbackContext):
    pass

def craft_meme_handler(update: Update, context: CallbackContext):
    pass

# MAIN HANDLER ------------------------------------------------
@log_error
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    print(context.user_data)
    stage = context.user_data.setdefault('stage', 0)
    page = context.user_data.setdefault('page', 1)
    id = context.user_data.setdefault('id', None)
    text0 = context.user_data.setdefault('text0', None)
    text1 = context.user_data.setdefault('text1', None)

    if text == btn_home:
        context.user_data.clear()
        # context.user_data['stage'] = 0
        # context.user_data['page'] = 1
        # context.user_data['if'] = None
        # context.user_data['text0'] = None
        # context.user_data['text1'] = None
        return start_handler(update, context)

    if stage == 0:
        if text == '/start':
            return start_handler(update, context)
        elif text == button_help:
            return button_help_handler(update, context)
        elif text == btn_start:
            return choose_meme_handler(update, context)

    if stage == 1:
        if text == btn_next_page:
            context.user_data['page'] += 1
            return other_page_handler(update, context)
        elif text == btn_prev_page:
            context.user_data['page'] -= 1
            return other_page_handler(update, context)
        else:
            for i in context.user_data['memes_list']:
                if text == i['name']:
                    context.user_data['id'] = i['id']
                    print(i['id'])
