class GuiAction:
    def __init__(self, metadata: dict) -> None:
        self.child_handlers = []
        self.layout = []
        self.metadata = metadata

    def handle(self, event, values, window):
        for child in self.child_handlers:
            child(event, values, window)
        self.handler(event, values, window)
        if event == 'OK':
            self.okay()

    def handler(self, event, values, window):
        pass

    def okay(self, event, values, window):
        pass

    def add_child(self, widget, handler):
        self.child_handlers.append(handler)
        if len(widget) > 1:
            self.layout = self.layout + widget
        else:
            self.layout.append(widget)