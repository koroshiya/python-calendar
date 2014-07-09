class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_event(self, event):
        raise NotImplementedError

    def processEvent(self, arg):
        raise NotImplementedError