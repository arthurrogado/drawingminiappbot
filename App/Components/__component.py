from telebot import TeleBot
from ..Utils import markups
from ..Database.database import DB

class BaseComponent():
    markup_cancel = markups.generate_inline([[['❌ Cancel', '*cancel']]])
    
    def __init__(self, bot: TeleBot, userid = None) -> None:
        self.bot = bot
        self.userid = userid
        self.db = DB(self.bot)

        self.bot.register_callback_query_handler(self.cancel, lambda call: call.data == '*cancel')

    def cancel(self, call):
        self.bot.answer_callback_query(call.id, '❌ Cancelled')
        self.bot.delete_message(call.message.chat.id, call.message.message_id)
        self.bot.clear_step_handler_by_chat_id(call.message.chat.id)
        self.bot.clear_callback_handlers_by_chat_id(call.message.chat.id)

    def goMainMenu(self, userid):
        from .main_menu import MainMenu
        MainMenu(self.bot, userid)