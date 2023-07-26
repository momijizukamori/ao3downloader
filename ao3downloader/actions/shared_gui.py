import datetime
from urllib.parse import unquote
import PySimpleGUI as sg

from ao3downloader import strings
from ao3downloader.fileio import FileOps
from ao3downloader.actions.shared import get_last_page_downloaded

class Widget:
    def __init__(self, key: str):
        self.key = key
    def handle(self, event, values, window):
        pass
    def render(self):
        pass

class BoolWidget(Widget):
    def __init__(self, key: str, label: str, default: bool = False, disabled: bool = False):
        self.label = label
        self.key = key
        self.value = default
        self.disabled = disabled

    def handle(self, event, values, window):
        if values:
            self.value = values.get(self.key, False)

    def render(self):
        return [[sg.Checkbox(self.label, self.default, k=self.key, disabled = self.disabled)]]


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
            filetype_checks.append(sg.Checkbox(filetype, is_checked, key=f'{self.prefix}{filetype}'))

        return [[sg.Frame(self.label, [filetype_checks])]]


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
        return [[sg.Input(key="pages", size=(4, 1)), sg.Text(strings.AO3_LABEL_PAGES)]]


def link(fileops: FileOps) -> str:
    layout = []
    link = get_last_page_downloaded(fileops, False)
    def handler(event, values, window):
        if values:
            window.metadata['link'] = values.get('link', None)
            if values.get('prev_link', None):
                window.metadata['link'] = link
            window.metadata['link_entered'] = len(values.get('link', '')) > 0
    if link:
        layout = layout + [[sg.Checkbox("Use last saved link?", k='prev_link', enable_events=True)],[sg.Text("Last saved link: "), sg.Text(unquote(link))]]

    return layout + [[sg.Text(strings.AO3_PROMPT_LINK), sg.Input(key='link', enable_events=True)]], handler


def pinboard_date() -> datetime.datetime:
    print(strings.PINBOARD_PROMPT_DATE)
    getdate = True if input() == strings.PROMPT_YES else False
    if getdate:
        date_format = 'mm/dd/yyyy'
        print(strings.PINBOARD_PROMPT_ENTER_DATE.format(date_format))
        inputdate = input()
        date = datetime.strptime(inputdate, '%m/%d/%Y')
    else:
        date = None
    return date


def back():
    return sg.Button("Back")

def save(disabled = False):
    return sg.Button("Save", disabled=disabled, key="save")

def output():
    return sg.Multiline(size=(50, 10), key='output', disabled=True, write_only = True, reroute_stdout=True, reroute_stderr=True, reroute_cprint=True, autoscroll=True, expand_x=True)

def can_login(values):
    return len(values.get("password", '')) > 0 and len(values.get("username", '')) > 0

def handle_login(metadata, repo, force = False):
    ao3_login = metadata.get('ao3_login', False)
    if ao3_login or force:
        username = metadata['username']
        password = metadata['password']
        try:
            repo.login(username, password)
            print("Ao3 login successful!")
        except Exception as e:
            print(f'Error trying to login: {e}')  


