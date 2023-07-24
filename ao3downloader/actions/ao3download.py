from ao3downloader import strings
from ao3downloader.actions import shared, shared_gui
from ao3downloader.ao3 import Ao3
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository

import PySimpleGUI as sg


def action():
    with Repository() as repo:
        fileops = FileOps()

        filetypes = shared.download_types(fileops)
        series = shared.series()
        link = shared.link(fileops)
        pages = shared.pages()
        images = shared.images()

        shared.ao3_login(repo, fileops)

        visited = shared.visited(fileops, filetypes)

        print(strings.AO3_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, filetypes, pages, series, images)
        ao3.download(link, visited)

def gui_action(metadata):
    fileops = FileOps()
    layout = []
    handlers = []

    disable_ao3 = not shared_gui.can_login(metadata)
    for widget, handler in [shared_gui.download_types(fileops), shared_gui.series(), shared_gui.link(fileops), shared_gui.pages(), shared_gui.images(), shared_gui.ao3_login(disable_ao3)]:
        layout = layout + widget
        handlers.append(handler)

    layout = layout + [[shared_gui.output()],
                    [shared_gui.back(), sg.OK(disabled=True)]]
    window = sg.Window("Save links", layout, metadata=metadata, finalize=True)

    def handler(event, values, window):
        for widget_handler in handlers:
            widget_handler(event, values, window)
        
        if values:
            state = len(values.get("link", '')) == 0 and not values.get('prev_link', None)
            window['OK'].update(disabled=state)
            
            if event == 'OK':
                with Repository() as repo:
                    fileops = FileOps()

                    pages = window.metadata['pages']
                    series = window.metadata['series']
                    images = window.metadata['images']
                    link = window.metadata['link']
                    filetypes = window.metadata['filetypes']

                    shared_gui.handle_login(window.metadata, repo)

                    visited = shared.visited(fileops, filetypes)

                    print(strings.AO3_INFO_DOWNLOADING)

                    ao3 = Ao3(repo, fileops, filetypes, pages, series, images)
                    ao3.download(link, visited)

    return window, handler