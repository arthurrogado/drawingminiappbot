# get_drawings_on.py
# it is a component that gets all drawings that a user is participating in

from telebot import TeleBot
from App.Components.__component import BaseComponent
from App.Database.drawings_on import DrawingOn
from App.Database.draw import Draw
from App.Utils.markups import markup_webapp_button
from App.Utils.constants import URL_DRAWINGS_ON

class GetDrawingsOn(BaseComponent):
    def __init__(self, bot: TeleBot, userid) -> None:
        super().__init__(bot)
        self.userid = userid
        self.start()

    def start(self):
        self.bot.send_message(self.userid, "⌛️ Getting drawings you are participating in!")
        # get the drawings from the database
        drawing_on = DrawingOn(self.bot)
        drawings_on_user = drawing_on.get_drawings_on_by_userid(self.userid)

        # getting info about drawings that user is participating in
        drawing = Draw(self.bot)
        drawings_on_info = drawing.get_draws_by_ids(tuple([drawing_on_user.get('id_drawing') for drawing_on_user in drawings_on_user]))

        markup = markup_webapp_button("👀 Click here to see your drawings", URL_DRAWINGS_ON, {'drawings_on': str(drawings_on_user), 'drawings_on_info': str(drawings_on_info)})
        if drawings_on_user:
            self.bot.send_message(self.userid, f"✅ Here are your drawings on you participate!", reply_markup=markup)
        else:
            self.bot.send_message(self.userid, "❌ You are not participating in any drawings!")

        self.goMainMenu(self.userid)