from telebot import TeleBot
from App.Components.__component import BaseComponent
from App.Database.draw import Draw
from App.Database.drawings_on import DrawingOn

class EnterDrawing(BaseComponent):
    def __init__(self, bot: TeleBot, userid=None, data=None) -> None:
        super().__init__(bot, userid)
        self.data = data

        self.start()

    def start(self):
        self.bot.send_message(self.userid, "⌛️ Entering drawing!")

        # verify if the user is the owner of the drawing
        drawing_list = Draw(self.bot).get_draw_by_id(self.data['drawing_id'])
        if drawing_list:
            drawing = drawing_list[0]
            if drawing.get('from_userid') == self.userid:
                self.bot.send_message(self.userid, "⚠️ You can't enter your own drawing!")
                return
        else:
            self.bot.send_message(self.userid, "❌ I can't find this drawing!")
            return

        # verify if the user is already participating in the drawing
        if DrawingOn(self.bot).verify_drawing_on(self.userid, self.data['drawing_id']) != []:
            self.bot.send_message(self.userid, "⚠️ You are already participating in this drawing! 🍀 Good luck!")
            return


        # add the user to the drawing
        result = DrawingOn(self.bot).add_drawing_on(self.userid, drawing.get('id'))
        if result:
            self.bot.send_message(self.userid, f"✅ You are now participating in the drawing!")
        else:
            self.bot.send_message(self.userid, "⚠️ Error entering drawing!")

        self.goMainMenu(self.userid)