from ao3downloader.actions.getlinks import GetLinksAction
from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import PagesWidget, LinkWidget, ao3_login, metadata, series, Back, Ok


class GetLinksGuiAction(GuiAction, GetLinksAction):
    key = 'l'
    desc = strings.ACTION_DESCRIPTION_LINKS_ONLY

    def __init__(self, settings: dict):
        super().__init__(settings, "Save links to file")
        self.add_child(LinkWidget(self.fileops))
        self.add_child(series())
        self.add_child(metadata())
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