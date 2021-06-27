from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from api.imgflip import get_memes, craft_meme, get_demo_meme
from .loger import log_error

# BUTTONS -----------------------------------------------------
button_help = '/help'
btn_start = '/choose_meme'
btn_next_page = '/next_page'
btn_prev_page = '/prev_page'
btn_back = '/back'
btn_home = '/home'
btn_confirm = '/confirm'
btn_yes = '/yes'
btn_no = '/no'
btn_ok = '/ok'
btn_empty = '/empty'

# KEYBOARDS ---------------------------------------------------
KB_START = [
    [
        KeyboardButton(text=button_help),
        KeyboardButton(text=btn_start)
    ],
]

KB_HOME = [
    [
        KeyboardButton(text=btn_empty),
    ],
    [
        KeyboardButton(text=btn_home),
        KeyboardButton(text=btn_back),
    ]
]

KB_CONFIRM = [
    [
        KeyboardButton(text=btn_no),
        KeyboardButton(text=btn_yes)
    ]
]

KB_OK = [
    [
        KeyboardButton(text=btn_ok),
    ]
]

# MARKUPS -----------------------------------------------------
MRK_START = ReplyKeyboardMarkup(
    keyboard=KB_START,
    resize_keyboard=True,
)
MRK_HOME = ReplyKeyboardMarkup(
    keyboard=KB_HOME,
    resize_keyboard=True,
)

MRK_CONFIRM = ReplyKeyboardMarkup(
    keyboard=KB_CONFIRM,
    resize_keyboard=True,
)

MRK_OK = ReplyKeyboardMarkup(
    keyboard=KB_OK,
    resize_keyboard=True,
)


# FUNCTIONS ---------------------------------------------------
def create_inline_kb(memes_list):
    kb = []
    for i in range(len(memes_list)):
        kb.append([
            InlineKeyboardButton(text=memes_list[i]['name'], callback_data=memes_list[i]['id'])
        ])
    return InlineKeyboardMarkup(kb)


# HANDLERS ----------------------------------------------------
def start_handler(update: Update, context: CallbackContext):
    context.user_data['stage'] = 0

    update.message.reply_text(
        text="Welcome to main menu of MemesCraft bot.",
        reply_markup=MRK_START
    )


def button_help_handler(update: Update, context: CallbackContext):
    context.user_data['stage'] = 0

    update.message.reply_text(
        text="Choose images from the list, then add captions.\nType /home in any unknown situation, to go to main menu.",
        reply_markup=MRK_START
    )


def choose_meme_handler(update: Update, context: CallbackContext):
    context.user_data['stage'] = 0
    try:
        memes = get_memes()
    except Exception:
        update.message.reply_text(
            text=f"Error {Exception}",
            reply_markup=MRK_START
        )
    context.user_data['memes_list'] = memes['data']['memes']
    keyboard = create_inline_kb(context.user_data['memes_list'])

    context.user_data['stage'] = 1

    update.message.reply_text(
        text=f"Choose your meme.",
        reply_markup=keyboard
    )


def get_text_handler(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        text=f"Enter text {context.user_data['box_current']}/{context.user_data['box_count']}\nYou can leave caption blank with /empty command.",
        reply_markup=MRK_HOME
    )


def confirm_meme_handler(update: Update, context: CallbackContext):
    txt = f"name: {context.user_data['name']}"
    i = 1
    while i <= context.user_data['box_count']:
        txt = txt + f'\ntext{i}: {context.user_data["boxes"][i - 1]}'
        i += 1
    update.message.reply_text(
        text=txt + "\nConfirm?",
        reply_markup=MRK_CONFIRM
    )


def craft_meme_handler(update: Update, context: CallbackContext):
    url = craft_meme(
        id=context.user_data['id'],
        text=context.user_data['boxes'],
    )
    update.message.reply_text(
        text=url,
        reply_markup=MRK_OK
    )


def callback_handler(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data
    for i in range(len(context.user_data['memes_list'])):
        if callback_data == context.user_data['memes_list'][i]['id']:
            context.user_data['id'] = context.user_data['memes_list'][i]['id']
            context.user_data['box_count'] = context.user_data['memes_list'][i]['box_count']
            context.user_data['name'] = context.user_data['memes_list'][i]['name']
            context.user_data['stage'] = 2
            update.callback_query.edit_message_text(
                text=update.effective_message.text,
                parse_mode=ParseMode.MARKDOWN
            )
            update.effective_message.reply_text(
                text=get_demo_meme(
                    meme_id=context.user_data['id'],
                    box_count=context.user_data['box_count']
                )
            )
            return get_text_handler(update=update, context=context)


# MAIN HANDLER ------------------------------------------------
@log_error
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    stage = context.user_data.setdefault('stage', 0)
    page = context.user_data.setdefault('page', 1)
    id = context.user_data.setdefault('id', None)
    name = context.user_data.setdefault('name', None)
    boxes = context.user_data.setdefault('boxes', [])
    box_count = context.user_data.setdefault('box_count', None)
    box_current = context.user_data.setdefault('box_current', 1)

    if text == btn_home:
        context.user_data.clear()
        return start_handler(update, context)

    if stage == 0:
        if text == '/start':
            return start_handler(update, context)
        elif text == button_help:
            return button_help_handler(update, context)
        elif text == btn_start:
            return choose_meme_handler(update, context)

    if stage == 2:
        while box_current <= box_count:
            if text == btn_back:
                context.user_data['box_current'] = 1
                return choose_meme_handler(update, context)
            elif text == btn_empty:
                context.user_data['boxes'].append('')
            else:
                context.user_data['boxes'].append(text)

            if box_current == box_count:
                break

            context.user_data['box_current'] += 1
            return get_text_handler(update, context)

        context.user_data['stage'] = 3
        return confirm_meme_handler(update, context)

    if stage == 3:
        if text == btn_yes:
            context.user_data['stage'] = 4
            return craft_meme_handler(update, context)
        elif text == btn_no:
            return choose_meme_handler(update, context)

    if stage == 4:
        context.user_data.clear()
        return start_handler(update, context)
