from ao3downloader.actions.markedforlater import MarkedForLaterAction
from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import FiletypeWidget, ao3_login, images, series, Back, Ok


class MarkedForLaterGuiAction(GuiAction, MarkedForLaterAction):
    key = 'm'
    desc = strings.ACTION_DESCRIPTION_MARKED_FOR_LATER

    def __init__(self, settings: dict):
        super().__init__(settings, "Save marked for later fics")
        self.add_child(FiletypeWidget(self.fileops))
        self.add_child(series())
        self.add_child(images())
        self.add_child(ao3_login())

    def buttons(self):
        self.layout.append([Back(), Ok()])

    def handler(self, event, values, window):
        if event == 'OK':
            self.action()
