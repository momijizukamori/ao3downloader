import csv
import datetime
import os
import PySimpleGUI as sg

from ao3downloader import strings
from ao3downloader.actions import shared, shared_gui
from ao3downloader.ao3 import Ao3
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository


def action():
    with Repository() as repo:
        fileops = FileOps()

        link = shared.link(fileops)
        series = shared.series()
        pages = shared.pages()
        metatdata = shared.metadata()

        shared.ao3_login(repo, fileops)

        ao3 = Ao3(repo, fileops, None, pages, series, False)
        links = ao3.get_work_links(link, metatdata)

        if metatdata:
            flattened = [flatten_dict(k, v) for k, v in links.items()]
            filename = f'links_{datetime.datetime.now().strftime("%m%d%Y%H%M%S")}.csv'
            with open(os.path.join(strings.DOWNLOAD_FOLDER_NAME, filename), 'w', newline='', encoding='utf-8') as f:
                keys = []
                sample = flattened[0]
                for key in sample: keys.append(key)
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                for item in flattened:
                    writer.writerow(item)
        else:
            filename = f'links_{datetime.datetime.now().strftime("%m%d%Y%H%M%S")}.txt'
            with open(os.path.join(strings.DOWNLOAD_FOLDER_NAME, filename), 'w') as f:
                for l in links:
                    f.write(l + '\n')


def flatten_dict(k: str, v: dict) -> dict:
    v['link'] = k
    return v

def gui_action(metadata):
    fileops = FileOps()
    layout = []
    handlers = []
    disable_ao3 = not shared_gui.can_login(metadata)
    for widget, handler in [shared_gui.ao3_login(disable_ao3), shared_gui.link(fileops), shared_gui.metadata(), shared_gui.series(), shared_gui.pages()]:
        layout = layout + widget
        handlers.append(handler)

    layout = layout + [[shared_gui.output()],
                    [shared_gui.back(), sg.OK(disabled=True)]]
    window = sg.Window("Save links", layout, metadata=metadata, finalize=True)

    def handler(event, values, window):
        for widget_handler in handlers:
            widget_handler(event, values, window)
        
        state = len(values["link"]) == 0 and len(window.metadata['link']) == 0
        window['OK'].update(disabled=state)
        
        if event == 'OK':
            with Repository() as repo:
                fileops = FileOps()
                pages = window.metadata['pages']
                series = window.metadata['series']
                link = window.metadata['link']
                metatdata = window.metadata['metadata']
                shared_gui.handle_login(window.metadata, repo)
                ao3 = Ao3(repo, fileops, None, pages, series, False)
                links = ao3.get_work_links(link, metatdata)

                if metatdata:
                    flattened = [flatten_dict(k, v) for k, v in links.items()]
                    filename = f'links_{datetime.datetime.now().strftime("%m%d%Y%H%M%S")}.csv'
                    with open(os.path.join(strings.DOWNLOAD_FOLDER_NAME, filename), 'w', newline='', encoding='utf-8') as f:
                        keys = []
                        sample = flattened[0]
                        for key in sample: keys.append(key)
                        writer = csv.DictWriter(f, fieldnames=keys)
                        writer.writeheader()
                        for item in flattened:
                            writer.writerow(item)
                else:
                    filename = f'links_{datetime.datetime.now().strftime("%m%d%Y%H%M%S")}.txt'
                    with open(os.path.join(strings.DOWNLOAD_FOLDER_NAME, filename), 'w') as f:
                        for l in links:
                            f.write(l + '\n')

    return window, handler
