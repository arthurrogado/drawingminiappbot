from telebot import TeleBot
from App.Components.__component import BaseComponent

class SendMessageToAll(BaseComponent):
    def __init__(self, bot: TeleBot, userid=None, data=None) -> None:
        super().__init__(bot, userid)
        self.data = data
        self.start()

    def start(self):
        self.bot.send_message(self.userid, "⌛️ Sending message to all users! This may take a while...")
        # get all users from drawing
        
        # 

        pass