from model.model import Model


class Todo(Model):
    def __init__(self, form):
        self.id = None
        self.username = form.get('username', '')
        self.title = form.get('title', '')
