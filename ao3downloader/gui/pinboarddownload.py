from ao3downloader.actions.pinboarddownload import PinboardDownloadAction
from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import FiletypeWidget, PinboardDateWidget, ao3_login, images, pinboard_exclude, Back, Ok


class PinboardDownloadGuiAction(GuiAction, PinboardDownloadAction):
    key = 'p'
    desc = strings.ACTION_DESCRIPTION_PINBOARD

    def __init__(self, settings: dict):
        super().__init__(settings, "Save fics from pinboard links")
        self.add_child(FiletypeWidget(self.fileops))
        self.add_child(images())
        self.add_child(pinboard_exclude())
        self.add_child(PinboardDateWidget())
        self.add_child(ao3_login())

    def buttons(self):
        self.layout.append([Back(), Ok()])

    def handler(self, event, values, window):
        if event == 'OK':
            self.action()
