import PySimpleGUI as sg

THREAD_KEY = '-THREAD-'
PROGRESS_START_KEY = '-START DOWNLOAD-'
PROGRESS_COUNT_KEY = '-COUNT-'
PROGRESS_END_KEY = '-END DOWNLOAD-'
PROGRESS_THREAD_EXITNG = '-THREAD EXITING-'

class GuiAction:
    def __init__(self, metadata: dict, title: str, output: bool = True, progress: bool = False) -> None:
        self.children = []
        self.layout = []
        self.metadata = metadata
        self.title = title
        self.outout = output
        self.progress = progress
        self.max_value = 0

    def handle(self, event, values, window):
        for child in self.children:
            child.handle(event, values, window)
        self.handler(event, values, window)
        if event == 'OK':
            self.okay()
        if event[0] == 'OUTPUT' and self.output:
            window['output'].update(event[1])
        if event[0] == 'PROGRESS' and self.progress:
            if event[1] == PROGRESS_START_KEY:
                self.max_value = values[event]
                window['progress'].unhide_row()
                window['progress'].update(0, self.max_value)
            elif event[1] == PROGRESS_COUNT_KEY:
                window['progress'].update(values[event]+1, self.max_value)


    def handler(self, event, values, window):
        pass

    def okay(self, event, values, window):
        pass

    def add_child(self, widget):
        self.children.append(widget)

    def render(self):
        layout = [child.render() for child in self.children]
        if self.progress:
            progress_bar = sg.ProgressBar(100, 'horizontal', size=(30,0), k='progress', expand_x=True)
            progress_bar.hide_row()
            layout.append([sg.pin(progress_bar)])
        if self.output:
            layout.append([sg.Text(k='output')])
        return sg.Window(self.title, layout + self.layout, metadata=self.metadata, finalize=True)
  