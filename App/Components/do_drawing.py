from telebot import TeleBot
import random

from App.Components.__component import BaseComponent
from App.Database.drawings_on import DrawingOn
from App.Database.draw import Draw


class DoDrawing(BaseComponent):
    def __init__(self, bot: TeleBot, userid=None, data=None) -> None:
        super().__init__(bot, userid)
        self.data = data
        self.start()

    def start(self):
        self.bot.send_message(self.userid, "⌛️ Drawing!")
        
        # get all users participating in the drawing
        all_participants = DrawingOn(self.bot).get_drawings_on_by_drawingid(self.data['drawing_id'])

        # get a random user from the list
        winner = random.choice(all_participants)
        self.bot.send_message(self.userid, f"🎉 The winner is: {winner.get('id_user')}!")

        # get drawing info
        drawing = Draw(self.bot).get_draw_by_id(self.data['drawing_id'])[0]

        # send a message to the winner
        try:
            message_text = f"🎉 Congratulations! You won the drawing {self.data['drawing_id']}!\n\n"
            message_text += f"🎁 Name: {drawing.get('name')}\n"
            message_text += f"📝 Description: {drawing.get('description')}\n"
            self.bot.send_message(winner.get('id_user'), message_text)
        except:
            self.bot.send_message(self.userid, f"⚠️ I couldn't send a message to the winner!")

        # set drawing as finished and set the winner
        if Draw(self.bot).set_winner_and_finish_draw(self.data['drawing_id'], winner.get('id_user')):
            self.bot.send_message(self.userid, f"✅ Drawing finished!")
        else:
            self.bot.send_message(self.userid, f"⚠️ Error finishing drawing!")

        self.goMainMenu(self.userid)