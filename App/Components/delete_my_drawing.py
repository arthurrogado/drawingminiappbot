from telebot import TeleBot
from App.Components.__component import BaseComponent
from App.Database.draw import Draw
from App.Utils.markups import generate_keyboard

class DeleteMyDrawging(BaseComponent):
    def __init__(self, bot: TeleBot, userid=None, data=None) -> None:
        super().__init__(bot, userid)
        self.data = data
        self.bot = bot
        self.start()

    def start(self):
        # Verify if the user is the owner of the drawing, if yes, continue, if not, return
        drawing_list = Draw(self.bot).get_draw_by_id(self.data['drawing_id'])
        if drawing_list[0]['from_userid'] != self.userid:
            self.bot.send_message(self.userid, "⚠️ You are not the owner of this drawing!")
            return
        
        # Confirm if the user wants to delete the drawing, using keyboard button
        markup = generate_keyboard([['⚠️ Yes, delete this drawing'],['No 😯']])
        first_confirmation_message = self.bot.send_message(self.userid, "⚠️ Are you sure you want to delete this drawing?", reply_markup=markup)
        self.bot.register_next_step_handler(first_confirmation_message, self.first_confirmation)

    def first_confirmation(self, message):
        if "Yes" in message.text:
            # Second confirmation, using keyboard button
            markup = generate_keyboard([['No 😯'],['⚠️ Yes, I\'m sure, delete this drawing']])
            second_confirmation_message = self.bot.send_message(self.userid, "⚠️ Are you *really* sure you want to delete this drawing?", parse_mode='MarkdownV2', reply_markup=markup)
            self.bot.register_next_step_handler(second_confirmation_message, self.second_confirmation)
        else:
            self.bot.send_message(self.userid, "⚠️ Drawing not deleted!")
            self.goMainMenu(self.userid)

    def second_confirmation(self, message):
        if "Yes" in message.text:
            # Delete the drawing
            if Draw(self.bot).delete_draw(self.data['drawing_id']):
                self.bot.send_message(self.userid, "✅ Drawing deleted!")
            else:
                self.bot.send_message(self.userid, "⚠️ Error deleting drawing!")
        else:
            self.bot.send_message(self.userid, "⚠️ Drawing not deleted!")

        self.goMainMenu(self.userid)
