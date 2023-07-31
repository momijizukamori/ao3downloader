from ao3downloader.actions.logvisualization import LogVisualizationAction
from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import Back, Ok


class LogVisualizationGuiAction(GuiAction, LogVisualizationAction):
    key = 'v'
    desc = strings.ACTION_DESCRIPTION_VISUALIZATION

    def __init__(self, settings: dict):
        super().__init__(settings, "Format logfiles")

    def buttons(self):
        self.layout.append([Back(), Ok()])

    def handler(self, event, values, window):
        if event == 'OK':
            self.action()
