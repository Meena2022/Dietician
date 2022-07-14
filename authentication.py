from flask_login import UserMixin

_user_id = 'test'
_password = 'pass'


class DieticianUser(UserMixin):

    def __init__(self):
        self._user_id = None
        self._password = None

    def set(self, user_id, password):
        self._user_id = user_id
        self._password = password
        return self

    def getUser(self, user_id):
        for i in range(len(users)):
            if users[i]._user_id == user_id:
                return users[i]
        return None

    def is_authenticated(self):
        return self._password == _password and self._user_id == _user_id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        if self._user_id == _user_id:
            return _user_id
        return ""


users = list()
user1 = DieticianUser().set(_user_id, _password)
users.append(user1)
