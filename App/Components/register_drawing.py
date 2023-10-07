from telebot import TeleBot
from App.Components.__component import BaseComponent
from uuid import uuid4
from App.Database.draw import Draw

class RegisterDrawing(BaseComponent):
    def __init__(self, bot: TeleBot, userid, data):
        super().__init__(bot)
        self.data = data
        self.userid = userid
        self.bot = bot

        self.start()

    def start(self):
        self.bot.send_message(self.userid, "⌛️ Registering new Drawing!")
        # create a identifier that is unique for each drawing
        # and will be used to share the drawing in link and QR code
        # limit the length of the identifier to 10 characters
        identifier = str(uuid4().int)[:10]
        # add the drawing to the database
        result = Draw(self.bot).add_draw(identifier, from_userid=self.userid, name=self.data['name'], description=self.data['description'])
        if result:
            self.bot.send_message(self.userid, f"✅ Drawing registered successfully\!\n\n*Identifier:* `{identifier}`", parse_mode='MarkdownV2')
            self.goMainMenu(self.userid)
        else:
            self.bot.send_message(self.userid, "❌ Error registering drawing!")