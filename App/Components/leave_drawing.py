from telebot import TeleBot
from App.Components.__component import BaseComponent
from App.Database.drawings_on import DrawingOn
from App.Database.draw import Draw
from App.Utils.markups import generate_inline, generate_keyboard

class LeaveDrawing(BaseComponent):
    def __init__(self, bot: TeleBot, userid=None, data=None) -> None:
        super().__init__(bot, userid)
        self.data = data
        
        print('********** LEAVE DRAWING DATA: ', self.data)

        self.start(self.data)

    def start(self, data):
        # Update the data
        # Avoids data retention from previous calls
        # I think this is a bug from the library: 
        # register_callback_query_handler keeps the data from previous calls in self.handle
        self.data = data

        # Confirm that the user wants to leave the drawing
        markup = generate_keyboard([
            ['⚠️ Yes'],
            ['No, keep me in!']
        ])

        msg_confirmation = self.bot.send_message(self.userid, "🤔 Are you sure you want to leave this drawing?", reply_markup=markup)
        # self.bot.register_callback_query_handler(self.handle, lambda call: call.data in [
        #     '*yes_leave_drawing',
        #     '*no_leave_drawing'
        # ])
        self.bot.register_next_step_handler(msg_confirmation, self.confirm_leave_drawing)

    def confirm_leave_drawing(self, message):
        if message.text == "Yes":
            self.bot.send_message(self.userid, "⌛️ Leaving drawing!")
            # verify if the user is participating in the drawing

            if DrawingOn(self.bot).verify_drawing_on(self.userid, self.data['drawing_id']) == []:
                self.bot.send_message(self.userid, "⚠️ You are not participating in this drawing!")
                return

            # verify if the drawing exists
            drawing_list = Draw(self.bot).get_draw_by_id(self.data['drawing_id'])
            if drawing_list:
                drawing = drawing_list[0]
                print('*************************************** DRAWING')
                print(drawing)
                # remove the user from the drawing
                result = DrawingOn(self.bot).remove_drawing_on(self.userid, drawing.get('id'))
                if result:
                    self.bot.send_message(self.userid, f"✅ You are no longer participating in the drawing!")
                else:
                    self.bot.send_message(self.userid, "⚠️ Error leaving drawing!")
            else:
                self.bot.send_message(self.userid, "❌ I can't find this drawing!")

        else:
            self.bot.send_message(self.userid, "👍 Ok, you are still participating in the drawing!")

        self.goMainMenu(self.userid)