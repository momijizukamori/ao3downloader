import datetime
import traceback
from urllib.parse import unquote
from PySimpleGUI import Text, FileBrowse, FolderBrowse, CalendarButton, Input, Button, Checkbox, Frame

from ao3downloader import strings
from ao3downloader.fileio import FileOps

class Widget:
    def __init__(self, key: str):
        self.key = key
    def handle(self, event, values, window):
        pass
    def render(self):
        pass

class BoolWidget(Widget):
    def __init__(self, label: str, key: str, default: bool = False, disabled: bool = False):
        self.label = label
        self.key = key
        self.value = default
        self.disabled = disabled

    def handle(self, event, values, window):
        if values:
            self.value = values.get(self.key, False)

    def render(self):
        return [[Checkbox(self.label, self.value, k=self.key, disabled = self.disabled)]]


def images() -> BoolWidget:
    return BoolWidget(strings.AO3_LABEL_IMAGES, 'images')


def metadata() -> BoolWidget:
    return BoolWidget(strings.AO3_LABEL_METADATA, 'metadata')


def ignorelist_check_deleted() -> BoolWidget:
    return BoolWidget(strings.IGNORELIST_LABEL_CHECK_DELETED, 'ignorelist_check_deleted')

def series() -> BoolWidget:
    return BoolWidget(strings.AO3_LABEL_SERIES, 'series')


def pinboard_exclude() -> BoolWidget:
    return BoolWidget(strings.PINBOARD_LABEL_INCLUDE_UNREAD, 'exclude_toread')


def ao3_login(disabled = False) -> BoolWidget:
    return BoolWidget(strings.AO3_LABEL_LOGIN, 'ao3_login', disabled=disabled)

class FiletypeWidget(Widget):
    def __init__(self, fileops: FileOps, label: str = strings.AO3_LABEL_DOWNLOAD_TYPE, prefix: str | None = None):
        self.default = fileops.get_setting(strings.SETTING_FILETYPES)
        self.avail = strings.AO3_ACCEPTABLE_DOWNLOAD_TYPES
        if prefix:
            self.prefix = prefix + "_"
        else:
            self.prefix = ''

        self.key = self.prefix + 'filetypes'
        self.label = label
        self.value = []

    def handle(self, event, values, window):
        filetypes = []
        if values:
            for filetype in self.avail:
                if values.get(f'{self.prefix}{filetype}', None):
                    filetypes.append(filetype)
            self.value = filetypes

    def render(self):
        filetype_checks = []
        for filetype in self.avail:
            is_checked = filetype in self.default
            filetype_checks.append(Checkbox(filetype, is_checked, key=f'{self.prefix}{filetype}'))

        return [[Frame(self.label, [filetype_checks])]]


class PagesWidget(Widget):
    def __init__(self):
        super.__init__(self, 'pages')

    def handle(self, event, values, window):
        if values:
            pages = values.get('pages', None)
            try:
                pages = int(pages)
                if pages <= 0:
                    pages = None
            except:
                pages = None
            
            self.value = pages

    def render(self):
        return [[Input(key="pages", size=(4, 1)), Text(strings.AO3_LABEL_PAGES)]]

class LinkWidget(Widget):
    def __init__(self, fileops: FileOps):
        super.__init__(self, 'link')
        self.prev = get_last_page_downloaded(fileops)
        self.value = None
        self.use_prev = False

    def handle(self, event, values, window):
        if values:
            self.value = values.get('link', None)
            self.use_prev = values.get('prev_link', False)
            if self.use_prev:
                self.value = self.prev
                window['link'].update(disabled = True)
            else:
                window['link'].update(disabled = False)

    def render(self):
        layout = []
        if self.prev:
            layout = layout + [[Checkbox("Use last saved link?", k='use_prev', enable_events=True)],[Text("Last saved link: "), Text(unquote(self.prev))]]
        return layout + [[Text(strings.AO3_PROMPT_LINK), Input(key='link', enable_events=True)]]

class FilePathWidget(Widget):
    def __init__(self):
        self.key = 'folder'

    def handle(self, event, values, window):
        if values:
            self.value = values.get(self.key, False)

    def render(self):
        return [[Text(strings.AO3_LABEL_FILE_INPUT)],
              [Input(key=self.key, enable_events=True), FileBrowse(file_types=(('Text files', "*.txt"), ('All Files', '*.* *')))]]
    
class FolderPathWidget(Widget):
    def __init__(self):
        self.key = 'folder'

    def handle(self, event, values, window):
        if values:
            self.value = values.get(self.key, None)

    def render(self):
        return [[Text(strings.AO3_LABEL_FILE_INPUT)],
              [Input(key=self.key, enable_events=True), FolderBrowse()]]


class PinboardDateWidget(Widget):
    def __init__(self):
        self.key = 'date'

    def handle(self, event, values, window):
        if values:
            date = values.get(self.key, None)
            if date:
                try:
                    self.value = datetime.strptime(date, '%m/%d/%Y')
                except:
                    self.log("Invalid date entered!")
                    self.value=None

    def render(self):
        return [[Text(strings.PINBOARD_PROMPT_ENTER_DATE.format('mm/dd/yyyy')), Input(key=self.key, enable_events=True), CalendarButton(format='%m/%d/%Y')]]


def Back():
    return Button("Back")

def Ok():
    return Button("Ok", key="OK")

def Save(disabled = False):
    return Button("Save", disabled=disabled, key="save")

# def output():
#     return sg.Multiline(size=(50, 10), key='output', disabled=True, write_only = True, reroute_stdout=True, reroute_stderr=True, reroute_cprint=True, autoscroll=True, expand_x=True)

class UsernameWidget(Widget):
    def __init__(self):
        self.key = 'username'

    def handle(self, event, values, window):
        if values:
            self.value = values.get(self.key, None)

    def render(self):
        return [[Text(strings.AO3_PROMPT_USERNAME),
              Input(key=self.key, enable_events=True)]]
    
class PasswordWidget(Widget):
    def __init__(self):
        self.key = 'password'

    def handle(self, event, values, window):
        if values:
            self.value = values.get(self.key, None)

    def render(self):
        return [[Text(strings.AO3_PROMPT_PASSWORD),
              Input(key=self.key, enable_events=True, password_char="*")]]
    
class PinboardTokenWidget(Widget):
    def __init__(self):
        self.key = 'password'

    def handle(self, event, values, window):
        if values:
            self.value = values.get(self.key, None)

    def render(self):
        return [[Text(strings.AO3_PROMPT_PASSWORD),
              Input(key=self.key, enable_events=True, password_char="*")]]


def can_login(values):
    return len(values.get("password", '')) > 0 and len(values.get("username", '')) > 0

def get_last_page_downloaded(fileops: FileOps) -> str:
    latest = None
    try:
        logs = fileops.load_logfile()
        starts = filter(lambda x: 'starting' in x, logs)
        bydate = sorted(starts, key=lambda x: datetime.datetime.strptime(x['timestamp'], '%m/%d/%Y, %H:%M:%S'), reverse=True)
        if bydate: latest = bydate[0]
    except Exception as e:
        fileops.write_log({'error': str(e), 'message': strings.ERROR_LOG_FILE, 'stacktrace': traceback.format_exc()})

    link = None
    if latest:
            link = latest['starting']

    return link