from telebot import TeleBot
from App.Database.database import DB
from App.Database.drawings_on import DrawingOn

class Draw(DB):
    def __init__(self, bot: TeleBot = None):
        super().__init__(bot)

    def add_draw(self, id, from_userid, name, description):
        return self.insert(
            'drawings',
            ['id', 'from_userid', 'name', 'description'],
            [id, from_userid, name, description]
        )
    
    def delete_draw(self, id):
        return self.delete(
            'drawings',
            f"id = ?",
            [id]
        )
    
    # generic functions to append participants number in each drawing
    # the only thing that changes is the where clause
    def get_drawings(self, where_clause, finished = 0):
        drawings = self.select(
            'drawings',
            ['id', 'from_userid', 'name', 'description'],
            where_clause + f" AND finished = {finished}"
        )
        # put participants number in each drawing
        for drawing in drawings:
            drawing['participants'] = DrawingOn.get_participants_number_in_drawing(self, drawing.get('id'))
        return drawings
    
    def get_draws_by_userid(self, userid):
        return self.get_drawings(f"from_userid = {userid}")
    
    def get_draw_by_id(self, identifier):
        return self.get_drawings(f"id = {identifier}")
    
    def get_draws_by_ids(self, identifiers: tuple):
            # remove the last comma from the tuple to avoid errors
            identifiers = str(identifiers).replace(',)', ')')
            return self.get_drawings(f"id IN {identifiers}")
    
    def get_my_finished_draws(self, userid):
        return self.get_drawings(f"from_userid = {userid}", 1)
    
    def update_draw(self, id, name, description):
        return self.update(
            'drawings',
            ['name', 'description'],
            [name, description],
            f"id = {id}"
        )
    
    def set_winner_and_finish_draw(self, id, winner):
        return self.update(
            'drawings',
            ['winner_user_id', 'finished'],
            [winner, 1],
            f"id = {id}"
        )