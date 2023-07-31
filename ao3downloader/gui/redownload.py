from ao3downloader.actions.redownload import RedownloadAction
from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import FiletypeWidget, ao3_login, Back, Ok


class RedownloadGuiAction(GuiAction, RedownloadAction):
    key = 'r'
    desc = strings.ACTION_DESCRIPTION_REDOWNLOAD

    def __init__(self, settings: dict):
        super().__init__(settings, "Download new filetype for existing fics", True)
        self.add_child(FiletypeWidget(self.fileops, label = strings.REDOWNLOAD_PROMPT_FILE_TYPE, prefix='old'))
        self.add_child(FiletypeWidget(self.fileops, label = strings.AO3_PROMPT_DOWNLOAD_TYPE, prefix='new'))
        self.add_child(ao3_login())

    def buttons(self):
        self.layout.append([Back(), Ok()])

    def handler(self, event, values, window):
        if event == 'OK':
            self.action()