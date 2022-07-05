from model.model import Model


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_register(self):
        # return True
        u = User.find_by(username=self.username)
        if u is not None:
            return False

    def validate_login(self):
        u = User.find_by(username=self.username)
        if u is not None:
            from utils import salted_password
            return u.password == salted_password(self.password)
        else:
            return False
