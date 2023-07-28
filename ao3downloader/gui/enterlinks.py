from ao3downloader.actions.enterlinks import EnterLinksAction
from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import FiletypeWidget, FilePathWidget, ao3_login, images, Back, Ok


class EnterLinksGuiAction(GuiAction, EnterLinksAction):
    key = 'f'
    desc = strings.ACTION_DESCRIPTION_FILE_INPUT

    def __init__(self, settings: dict):
        super().__init__(settings, "Download links from file", True)
        self.add_child(FiletypeWidget(self.fileops))
        self.add_child(images())
        self.add_child(ao3_login())
        self.add_child(FilePathWidget())

    def buttons(self):
        self.layout.append([Back(), Ok()])

    def handler(self, event, values, window):
        if event == 'path':
            state = len(self.file_path()) == 0
            window['OK'].update(disabled=state)
        if event == 'OK':
            self.action()
