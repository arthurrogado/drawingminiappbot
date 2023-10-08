from telebot import TeleBot
from App.Database.database import DB

class DrawingOn(DB):
    def __init__(self, bot: TeleBot = None):
        super().__init__(bot)

    def add_drawing_on(self, userid, drawingid):
        # verify if the user is already participating in the drawing
        if self.select(
            'drawings_on',
            ['id_user', 'id_drawing'],
            f"id_user = {userid} AND id_drawing = {drawingid}"
        ):
            return False
            
        return self.insert(
            'drawings_on',
            ['id_user', 'id_drawing'],
            [userid, drawingid]
        )
    
    def verify_drawing_on(self, userid, drawingid):
        return self.select(
            'drawings_on',
            ['id_user', 'id_drawing'],
            f"id_user = {userid} AND id_drawing = {drawingid}"
        )
    
    def get_drawings_on_by_userid(self, userid):
        return self.select(
            'drawings_on',
            ['id_user', 'id_drawing'],
            f"id_user = {userid}"
        )
    
    def get_drawings_on_by_drawingid(self, drawingid):
        return self.select(
            'drawings_on',
            ['id_user', 'id_drawing'],
            f"id_drawing = {drawingid}"
        )
    
    def get_participants_number_in_drawing(self, drawingid):
        return len(self.select(
            'drawings_on',
            ['id_user', 'id_drawing'],
            f"id_drawing = {drawingid}"
        ))
    
    def get_users_in_drawing(self, drawingid):
        return self.select(
            'drawings_on',
            ['id_user', 'id_drawing'],
            f"id_drawing = {drawingid}"
        )
    
    def remove_drawing_on(self, userid, drawingid):
        return self.delete(
            'drawings_on',
            f"id_user = ? AND id_drawing = ?",
            [userid, drawingid]
        )