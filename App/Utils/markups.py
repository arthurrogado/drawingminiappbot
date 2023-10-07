from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    WebAppInfo
)
from .functions import dict_to_url_params
from App.Database.draw import Draw

def replyKeyboardMarkup(**kwargs) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(**kwargs)

def inlineKeyboardMarkup(**kwargs) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(**kwargs)

def inlineKeyboardButton(text: str, callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback_data)

def keyboardButton(text: str) -> KeyboardButton:
    return KeyboardButton(text=text)

def generate_inline(buttons: list, sufix: str = ''):
    ### Example:
    # buttons = [ # scope
    #     [ # line
    #         ['Butto1', 'action1'], # button
    #         ['Butto2', 'action2'],
    #     ],
    #     [
    #         ['Butto3', 'action3'],
    #         ['Butto4', 'action4'],
    #         ['Butto5', 'action5']
    #     ]
    # ]
    # sufix: str = _id
    markup = InlineKeyboardMarkup()
    for line in buttons:
        markup.row(
            *[InlineKeyboardButton(text=button[0], callback_data=f'{button[1]}{sufix}') for button in line]
        )
    return markup

def generate_keyboard(buttons: list, **kwargs) -> ReplyKeyboardMarkup:
    ### Example:
    # buttons = [
    #     ['Button1', 'Button2'],
    #     ['Button3', 'Button4', 'Button5']
    # ]
    markup = ReplyKeyboardMarkup(**kwargs, one_time_keyboard=True)
    for line in buttons:
        markup.row(
            *[KeyboardButton(text=button) for button in line]
        )
    return markup

def clearKeyboard():
    return ReplyKeyboardRemove()

def markup_webapp_button(text, baseurl, params: dict = None, userid: int = None):
    # append basic information to params, like: my_drawings, drawings_i_participate, etc
    draw = Draw()
    if userid:
        my_drawings = draw.get_draws_by_userid(userid)
        params['my_drawings'] = str(my_drawings)

    url = baseurl + dict_to_url_params(params) if params else baseurl
    # print('PARAMS', params)
    # print("BASEURL", baseurl)
    # print('URL', url)
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(KeyboardButton(text, web_app=WebAppInfo(url=url)))
    return markup