from telebot import TeleBot
from App.Database.database import DB

class User(DB):
    def __init__(self, bot: TeleBot = None):
        super().__init__(bot)
    
    def add_user(self, userid, name, birthday):
        return self.insert('users', ['userid', 'name', 'birthday'], [userid, name, birthday])

    def get_user(self, userid):
        return self.select('users', ['*'], 'userid = ?', [userid])

    def update_user(self, userid, name, birthday):
        return self.update('users', ['name', 'birthday'], 'userid = ?', [userid])

    def delete_user(self, userid):
        return self.delete('users', 'userid = ?', [userid])