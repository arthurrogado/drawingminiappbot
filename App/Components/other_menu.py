from telebot import TeleBot
from App.Components.__component import BaseComponent
from ..Utils.markups import *

class OtherMenu(BaseComponent):

    def __init__(self, bot: TeleBot, userid):
        super().__init__(bot, userid)
        self.bot = bot
        self.userid = userid

        self.start()

    def start(self):
        msg = self.bot.send_message(self.userid, "*OTHER MENU\!*", parse_mode='MarkdownV2', reply_markup=generate_keyboard([['Hello other!']]))
        self.bot.register_next_step_handler(msg, self.handle)

    def handle(self, msg):
        self.bot.send_message(self.userid, "Hello another!", reply_markup=clearKeyboard())
        # clear keyboard markup