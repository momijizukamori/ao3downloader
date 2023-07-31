from typing import Callable, Iterator
from PySimpleGUI import Window, Text, ProgressBar, pin
from datetime import datetime
import traceback
import time

from ao3downloader.actions.BaseAction import BaseAction
from ao3downloader.gui.shared_gui import Widget
from ao3downloader.fileio import FileOps
from ao3downloader import strings

THREAD_KEY = 'PROGRESS'
PROGRESS_START_KEY = '-START DOWNLOAD-'
PROGRESS_COUNT_KEY = '-COUNT-'
PROGRESS_END_KEY = '-END DOWNLOAD-'
PROGRESS_THREAD_EXITNG = '-THREAD EXITING-'

class GuiAction(BaseAction):
    def __init__(self, metadata: dict, title: str, progress: bool = False) -> None:
        self.children: list[Widget] = []
        self.layout = []
        self.settings = metadata
        self.title = title
        self.show_progress = progress
        self.max_value = 0
        self.fileops = FileOps()

    def handle(self, event, values, window):
        for child in self.children:
            child.handle(event, values, window)
        self.handler(event, values, window)
        if event == 'OUTPUT':
            window['output'].update(values['OUTPUT'])
        if event[0] == 'PROGRESS' and self.show_progress:
            if event[1] == PROGRESS_START_KEY:
                self.max_value = values[event]
                # window['progress'].set_size((10))
                window['progress'].update(0, self.max_value)
            elif event[1] == PROGRESS_COUNT_KEY:
                window['progress'].update(values[event], self.max_value)
            elif event[1] == PROGRESS_END_KEY:
                self.log("Done!")

    def handler(self, event, values: list[any], window):
        pass

    def add_child(self, widget: Widget) -> None:
        self.children.append(widget)

    def render(self) -> Window:
        layout = [child.render() for child in self.children]
        if self.show_progress:
            progress_bar = ProgressBar(100, 'horizontal', size=(30, 10), k='progress', expand_x=True)
            # progress_bar.hide_row()
            layout.append([pin(progress_bar)])

        layout.append([Text(k='output', expand_x=True, justification='center')])
        self.buttons()
        self.window = Window(self.title, layout + self.layout, metadata=self.metadata, finalize=True)
        return self.window

    def get_value(self, key: str, default: any) -> any:
        for child in self.children:
            if child.key == key:
                return child.value
        return default
    
    def log(self, text: str) -> None:
        self.window['output'].update(text)

    def pages(self) -> int:
        return self.get_value('pages')
    
    def link(self) -> str | None:
        return self.get_value('link', None)
  
    def images(self) -> bool:
        return self.get_value('images', False)

    def series(self) -> bool:
        return self.get_value('series', False)

    def metadata(self) -> bool:
        return self.get_value('metadata', False)

    def ignorelist_check_deleted(self) -> bool:
        return self.get_value('ignorelist_check_deleted', False)

    def pinboard_exclude(self) -> bool:
        return self.get_value('pinboard_exclude', False)

    def redownload_oldtypes(self) -> list[str]:
        return self.get_value('old_filetypes', [])

    def redownload_newtypes(self) -> list[str]:
        return self.get_value('new_filetypes', [])

    def download_types(self) -> list[str]:
        return self.get_value('filetypes', [])

    def update_types(self) -> list[str]:
        return self.get_value('update_filetypes')

    def pinboard_date(self) -> datetime | None:
        return self.get_value('date', None)

    def redownload_folder(self) -> str:
        return self.get_value('folder', '')

    def update_folder(self) -> str:
        return self.get_value('folder', '')
    
    def file_path(self) -> str:
        return self.get_value('path', '')

    def ao3_login(self, repo, force = False):
        ao3_login = self.get_value('ao3_login', False)
        if ao3_login or force:
            username = self.settings['username']
            password = self.settings['password']
            try:
                repo.login(username, password)
                self.log("Ao3 login successful!")
            except Exception as e:
                self.log(f'Error trying to login: {e}')  

    def buttons(self) -> None:
        pass

    def progress(self, callback: Callable[..., any], iterator: Iterator) -> None:
        self.window.start_thread(lambda: self.progress_action(self.window, callback, iterator), (THREAD_KEY, PROGRESS_THREAD_EXITNG))
    
    def progress_action(self, window, callback: Callable, iterator: Iterator):
        """
        The thread that communicates with the application through the window's events.
        """
        max_value = len(iterator)
        count = 1
        window.write_event_value((THREAD_KEY, PROGRESS_START_KEY), max_value)  # Data sent is a tuple of thread name and counter
        for i in iterator:
            window.write_event_value((THREAD_KEY, PROGRESS_COUNT_KEY), count)
            window.write_event_value('OUTPUT', f'{count} of {max_value}')
            callback(i)
            time.sleep(1)

            count = count + 1  # Data sent is a tuple of thread name and counter
        window.write_event_value((THREAD_KEY, PROGRESS_END_KEY), max_value)  # Data sent is a tuple of thread name and counter

    def get_last_page_downloaded(self) -> str:
        latest = None
        try:
            logs = self.fileops.load_logfile()
            starts = filter(lambda x: 'starting' in x, logs)
            bydate = sorted(starts, key=lambda x: datetime.datetime.strptime(x['timestamp'], '%m/%d/%Y, %H:%M:%S'), reverse=True)
            if bydate: latest = bydate[0]
        except Exception as e:
            self.fileops.write_log({'error': str(e), 'message': strings.ERROR_LOG_FILE, 'stacktrace': traceback.format_exc()})

        link = None
        if latest:
                link = latest['starting']

        return link