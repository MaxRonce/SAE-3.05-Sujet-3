from .app import db, login_manager
from flask_login import UserMixin
import link_front_back.db_link as db_link

class User(UserMixin):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

    def __repr__(self):
        return f"name: {self.username}, pw: {self.password}"


@login_manager.user_loader
def load_user(username):
    if username is None:
        return None
    u = db_link.ses.query(db_link.User).filter(db_link.User.idUser == username).one()
    us = User(u.idUser, u.mdpUser)
    return us


