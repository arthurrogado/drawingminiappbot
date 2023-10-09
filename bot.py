from telebot import TeleBot
from telebot.types import (
    Message,
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
    MenuButtonCommands
)

from App.Database.database import DB
from App.Config.config import *
from App.Utils.markups import *

# Models
from App.Database.users import User

# Components
from App.Components.main_menu import MainMenu
from App.Components.register_drawing import RegisterDrawing
from App.Components.get_my_drawings import GetMyDrawings
from App.Components.update_drawing import UpdateDrawing
from App.Components.get_drawings_on import GetDrawingsOn
from App.Components.enter_drawing import EnterDrawing
from App.Components.leave_drawing import LeaveDrawing
from App.Components.do_drawing import DoDrawing
from App.Components.delete_my_drawing import DeleteMyDrawging
from App.Components.send_message_to_all import SendMessageToAll

import json

bot = TeleBot(BOT_TOKEN)


# Set basic commands (start, about, help)
basic_commands = [
    BotCommand("start", "🤖 Start botttttt"),
    BotCommand("about", "❓ About the bot"),
    BotCommand("help", "📚 Help")
]
bot.set_my_commands(basic_commands, scope = BotCommandScopeAllPrivateChats() )
bot.set_chat_menu_button(menu_button=MenuButtonCommands(type="commands"))


# WebApp messages handler
@bot.message_handler(content_types="web_app_data")
def answer(msg):
    userid = msg.from_user.id
    try:
        response = json.loads(msg.web_app_data.data)
        # clear keyboard
        bot.send_message(msg.from_user.id, 'Success! Data received: \n\n' + str(response), reply_markup=ReplyKeyboardRemove())

        action = response.get('action')

        if action == 'register_drawing':
            RegisterDrawing(bot, userid, response)
        elif action == 'delete_my_drawing':
            DeleteMyDrawging(bot, userid, response)
        elif action == 'get_my_drawings':
            GetMyDrawings(bot, userid)
        elif action == "update_drawing":
            UpdateDrawing(bot, userid, response)
        elif action == "get_drawings_on":
            GetDrawingsOn(bot, userid)
        elif action == "enter_drawing":
            EnterDrawing(bot, userid, response)
        elif action == "leave_drawing":
            LeaveDrawing(bot, userid, response)
        elif action == "do_drawing":
            DoDrawing(bot, userid, response)
        elif action == "send_message_to_all":
            SendMessageToAll(bot, userid, response) # response = {'message': 'message to send', 'drawing_id': 'id of the drawing'}

    except Exception as e:
        print("#Error", e)
        # get line of error
        import traceback
        traceback.print_exc()

        response = msg.web_app_data.data
        bot.send_message(msg.from_user.id, 'Error, but data: \n\n' + response)


# /teste : comando com ação específica para teste
@bot.message_handler(commands=['test'])
def teste(msg):
    userid = msg.chat.id
    bot.send_message(userid, 'Test')


# Any message
@bot.message_handler(func= lambda m: True)
def receber(msg: Message):
    userid = msg.from_user.id

    # custom start message
    split = msg.text.split()
    if len(split) > 1:
        if split[0] == '/start' and split[1].startswith('drawing_id='):
            bot.send_message(userid, "Welcome to the bot!")
            EnterDrawing(bot, userid, {'drawing_id': split[1].split('=')[1]})
            return
        
    elif msg.text == "/about":
        bot.send_message(userid, "About the bot")
        msg_about = "This bot is an example of a bot that uses the WebApp feature (Mini App).\n\n"
        msg_about += "It helps you manage drawings.\n"
        msg_about += "You can create drawings and invite people to participate.\n"
        msg_about += "You can also participate in drawings created by other people.\n\n"
        msg_about += "This bot was created by @arthurrogado\n"
        msg_about += "Source code: https://github.com/arthurrogado/drawingminiappbot"
        bot.send_message(userid, msg_about)
        return
    
    elif msg.text == "/help":
        bot.send_message(userid, "Help")
        msg_help = "Commands:\n"
        msg_help += "/start - Start the bot\n"
        msg_help += "/about - About the bot\n"
        msg_help += "/help - Help\n"
        bot.send_message(userid, msg_help)
        return

    MainMenu(bot=bot, userid=userid)

    # # Verify if user exists
    # if db.verify_user(userid) == False:
    #     db.add_user(userid, user.first_name, user.username, user.language_code.split('-')[0] )


# CALLBACKS
@bot.callback_query_handler(func=lambda call: call.data.startswith('*') == False)
def callback(call):
    userid = call.from_user.id
    data = call.data

    options = {
        'hello': lambda: bot.answer_callback_query(call.id, f'Olá {call.from_user.first_name}'),
    }

    if data in options:
        options[data]() # Executes the function in the dict

bot.infinity_polling()