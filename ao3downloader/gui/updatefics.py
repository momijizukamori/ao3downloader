from ao3downloader.actions.updatefics import UpdateFicsAction
from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import FiletypeWidget, FolderPathWidget, ao3_login, images, Back, Ok


class UpdateFicsGuiAction(GuiAction, UpdateFicsAction):
    key = 'u'
    desc = strings.ACTION_DESCRIPTION_UPDATE

    def __init__(self, settings: dict):
        super().__init__(settings, "Update saved fics", True)
        self.add_child(FiletypeWidget(self.fileops, label = strings.AO3_PROMPT_DOWNLOAD_TYPE, prefix="update"))
        self.add_child(FiletypeWidget(self.fileops))
        self.add_child(FolderPathWidget())
        self.add_child(images())
        self.add_child(ao3_login())

    def buttons(self):
        self.layout.append([Back(), Ok()])

    def handler(self, event, values, window):
        if event == 'folder':
            state = len(self.update_folder()) == 0
            window['OK'].update(disabled=state)
        if event == 'OK':
            self.action()