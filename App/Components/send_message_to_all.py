from telebot import TeleBot
from App.Components.__component import BaseComponent
from App.Database.drawings_on import DrawingOn

class SendMessageToAll(BaseComponent):
    def __init__(self, bot: TeleBot, userid=None, data=None) -> None:
        super().__init__(bot, userid)
        self.data = data # response = {'message': 'message to send', 'drawing_id': 'id of the drawing'}
        self.start()

    def start(self):
        # get all users from drawing
        users = DrawingOn(self.bot).get_users_in_drawing(self.data['drawing_id'])
        # send message to all users
        # create a counting variable to show the progress
        count = 0
        count_failed = 0
        total = len(users)
        count_msg = self.bot.send_message(self.userid, f"⌛️ Sending message to {total} users! This may take a while...")
        for user in users:
            try:
                self.bot.send_message(user['id_user'], self.data['message'])
                count += 1
                self.bot.edit_message_text(f"⌛️ Sending message to {total} users! This may take a while...\n\n{count}/{total} users sent!", self.userid, count_msg.message_id)
            except:
                count_failed += 1
                self.bot.edit_message_text(f"⌛️ Sending message to {total} users! This may take a while...\n\n{count}/{total} users sent!\n\n{count_failed} users failed!", self.userid, count_msg.message_id)
                pass
        
        self.bot.send_message(self.userid, f"✅ Message sent to {count}/{total} users!\n\n{count_failed} users failed!")