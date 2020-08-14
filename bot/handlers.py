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
        ],
        [
            KeyboardButton(text=btn_home),
        ]
    ]
    if page == 1:
        del keyboard[2][0]
    elif page == 25:
        del keyboard[2][1]
    return keyboard


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
    keyboard = create_kb(context.user_data['memes_list'], context.user_data['page'])

    MRK_MEMES_LIST = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

    context.user_data['stage'] = 1

    update.message.reply_text(
        text=f"Choose your meme\nYou are currently on page {context.user_data['page']}/25",
        reply_markup=MRK_MEMES_LIST
    )





def other_page_handler(update: Update, context: CallbackContext):
    keyboard = create_kb(context.user_data['memes_list'], context.user_data['page'])

    MRK_MEMES_LIST = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

    update.message.reply_text(
        text=f"Choose your meme\nYou are currently on page {context.user_data['page']}/25",
        reply_markup=MRK_MEMES_LIST
    )
def get_text_handler(update: Update, context: CallbackContext):
    # context.user_data['stage'] = 3
    update.message.reply_text(
        text=f"Enter text {context.user_data['box_current']}/{context.user_data['box_count']}\nYou can leave caption blank with /empty command.",
        reply_markup=MRK_HOME
    )

# def get_text1_handler(update: Update, context: CallbackContext):
#     update.message.reply_text(
#         text="Add second line of text for meme",
#         reply_markup=MRK_HOME
#     )

def confirm_meme_handler(update: Update, context: CallbackContext):
    # context.user_data['stage'] += 1
    txt = f"name: {context.user_data['name']}"
    i = 1
    while i <= context.user_data['box_count']:
        txt = txt + f'\ntext{i}: {context.user_data["boxes"][i-1]}'
        i += 1
    update.message.reply_text(
        text=txt + "\nConfirm?",
        reply_markup=MRK_CONFIRM
    )

def craft_meme_handler(update: Update, context: CallbackContext):
    # context.user_data['stage'] = 7
    url = craft_meme(
        id=context.user_data['id'],
        text=context.user_data['boxes'],
    )
    update.message.reply_text(
        text=url,
        reply_markup=MRK_OK
    )


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

    print(context.user_data)

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
                    context.user_data['box_count'] = i['box_count']
                    context.user_data['name'] = text
                    context.user_data['stage'] = 2
                    return get_text_handler(update, context)

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
