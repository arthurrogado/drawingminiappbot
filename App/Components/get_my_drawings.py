from telebot import TeleBot
from App.Components.__component import BaseComponent
from App.Database.draw import Draw
from App.Utils.constants import URL_MY_DRAWINGS
from App.Utils.markups import markup_webapp_button

class GetMyDrawings(BaseComponent):
    def __init__(self, bot: TeleBot, userid) -> None:
        super().__init__(bot)
        self.userid = userid
        self.start()

    def start(self):
        self.bot.send_message(self.userid, "⌛️ Getting your drawings!")
        # get the drawings from the database
        result = Draw(self.bot).get_draws_by_userid(self.userid)
        # create a keyboard button that opens webapp drawings page
        # and passes drawings data in url parameters
        markup = markup_webapp_button("👀 Click here to see your drawings", URL_MY_DRAWINGS, {'my_drawings': str(result)})
        if result:
            self.bot.send_message(self.userid, f"✅ Here are your drawings\!", reply_markup=markup)
        else:
            self.bot.send_message(self.userid, "❌ You don't have any drawings\!")

        self.goMainMenu(self.userid)