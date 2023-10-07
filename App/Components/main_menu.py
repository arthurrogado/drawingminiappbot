from telebot import TeleBot
from telebot.types import CallbackQuery
from App.Components.__component import BaseComponent
from App.Components.other_menu import OtherMenu
from ..Utils.markups import *
from ..Utils.constants import URL_HOME, URL_CREATE_DRAW

from App.Database.draw import Draw
from App.Database.drawings_on import DrawingOn

class MainMenu(BaseComponent):

    def __init__(self, bot: TeleBot, userid):
        super().__init__(bot)
        self.bot = bot
        self.userid = userid
        self.start()

    def start(self):
        # EXAMPLE: Generate a simple inline keyboard
        # self.bot.send_message(self.userid, "*MAIN MENU\!*", parse_mode='MarkdownV2', reply_markup=generate_inline([
        #     [['>START MINI APP<', '*miniapp']],
        # ]))

        # get basic info: my drawings, drawings on...
        my_drawings = Draw(self.bot).get_draws_by_userid(self.userid)
        drawings_on = DrawingOn(self.bot).get_drawings_on_by_userid(self.userid)
        drawings_on_info = Draw(self.bot).get_draws_by_ids(tuple([drawing_on_user.get('id_drawing') for drawing_on_user in drawings_on]))
        
        # This are the parameters that will be passed to the webapp and won't be replaced in webapp routes
        # see webapp > app.js > getStartParams
        mainParams = {
            'bot_username': str(self.bot.get_me().username),
            'my_drawings': str(my_drawings),
            'drawings_on': str(drawings_on),
            'drawings_on_info': str(drawings_on_info)
        }

        self.markup_start_info = markup_webapp_button("👉 Open Drawing Mini App!", URL_HOME, mainParams)
        self.bot.send_message(self.userid, "*🍀 Drawing Mini App\!*", parse_mode='MarkdownV2', reply_markup=self.markup_start_info)

        # EXAMPLE: if you use callback queries
        # self.bot.register_callback_query_handler(self.handle, lambda call: call.data in [
        #     '*miniapp', 
        #     '*new_drawing'
        # ])

    # Example of how you can set a callback query handler
    def handle(self, call: CallbackQuery):
        self.userid = call.from_user.id
        
        if call.data == "*miniapp":
            self.bot.send_message(self.userid, "🍀 Drawing Mini App!", reply_markup=self.markup_start_info)

        elif call.data == "*new_drawing":
            markup = markup_webapp_button("New Drawing", URL_CREATE_DRAW)
            self.bot.send_message(self.userid, "New Drawing!", reply_markup=markup)

