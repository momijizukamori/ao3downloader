from ao3downloader import strings
from ao3downloader.actions import shared, shared_gui
from ao3downloader.ao3 import Ao3
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository

from tqdm import tqdm
import PySimpleGUI as sg

def action():
    with Repository() as repo:
        fileops = FileOps()

        filetypes = shared.download_types(fileops)
        images = shared.images()

        print(strings.AO3_PROMPT_FILE_INPUT)
        path = input()
        with open(path) as f:
            links = f.readlines()

        shared.ao3_login(repo, fileops)

        visited = shared.visited(fileops, filetypes)

        print(strings.AO3_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, filetypes, 0, True, images)
        for link in tqdm(links):
            ao3.download(link.strip(), visited)

def gui_action(metadata):
    fileops = FileOps()
    layout = []
    handlers = []
    disable_ao3 = not shared_gui.can_login(metadata)
    for widget, handler in [shared_gui.ao3_login(disable_ao3), shared_gui.download_types(fileops), shared_gui.images()]:
        layout = layout + widget
        handlers.append(handler)

    def enterlinks_handler(event, values, window):
        for widget_handler in handlers:
            widget_handler(event, values, window)
        path = values['path']
        if event == 'path':
            state = len(path) == 0
            window['OK'].update(disabled=state)
        if event == 'OK':
            with Repository() as repo:
                fileops = FileOps()
                with open(path) as f:
                    links = f.readlines()

                shared_gui.handle_login(window.metadata, repo)

                visited = shared.visited(fileops, window.metadata['filetypes'])

                print(strings.AO3_INFO_DOWNLOADING)

                ao3 = Ao3(repo, fileops, window.metadata['filetypes'], 0, True, window.metadata['images'])
                for link in tqdm(links):
                    ao3.download(link.strip(), visited)

    layout = layout + [
              [sg.Text(strings.AO3_LABEL_FILE_INPUT)],
              [sg.Input(key="path", enable_events=True), sg.FileBrowse(file_types=(('Text files', "*.txt"), ('All Files', '*.* *')))],
              [shared_gui.output()],
              [sg.OK(disabled=True), shared_gui.back()]]
    window = sg.Window("Download Links", layout, metadata=metadata, finalize=True)
    return window, enterlinks_handler