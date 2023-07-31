from ao3downloader.actions.ao3download import Ao3DownloadAction
from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import FiletypeWidget, PagesWidget, LinkWidget, ao3_login, images, series, Back, Ok


class Ao3DownloadGuiAction(GuiAction, Ao3DownloadAction):
    key = 'a'
    desc = strings.ACTION_DESCRIPTION_AO3

    def __init__(self, settings: dict):
        super().__init__(settings, "Download fics from link")
        self.add_child(FiletypeWidget(self.fileops))
        self.add_child(LinkWidget(self.fileops))
        self.add_child(series())
        self.add_child(images())
        self.add_child(ao3_login())
        self.add_child(PagesWidget())

    def buttons(self):
        self.layout.append([Back(), Ok()])

    def handler(self, event, values, window):
        if event == 'link' or event == 'use_prev':
            state = len(self.link()) == 0
            window['OK'].update(disabled=state)
        if event == 'OK':
            self.action()
