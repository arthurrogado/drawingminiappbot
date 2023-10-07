from telebot import TeleBot
from App.Components.__component import BaseComponent
from App.Database.draw import Draw
from App.Utils.markups import markup_webapp_button
from App.Utils.constants import URL_VIEW_DRAWING

class UpdateDrawing(BaseComponent):
    def __init__(self, bot: TeleBot, userid, data):
        super().__init__(bot)
        self.data = data
        self.userid = userid

        self.start()

    def start(self):
        self.bot.send_message(self.userid, '⏳ Updating drawing!')
        # update the drawing in the database
        if Draw(self.bot).update_draw(self.data['id'], self.data['name'], self.data['description']):
            self.bot.send_message(self.userid, '✅ Drawing updated successfully!')
        else:
            self.bot.send_message(self.userid, '❌ Error updating drawing!')

        # Send a button to open the webapp in view_drawing:
        markup = markup_webapp_button("👀 Click here to see your drawing", URL_VIEW_DRAWING, {'id_view_drawing': self.data['id']}, userid=self.userid)
        self.bot.send_message(self.userid, '⬇️ Click below to see this drawing.', reply_markup=markup)

        self.goMainMenu(self.userid)