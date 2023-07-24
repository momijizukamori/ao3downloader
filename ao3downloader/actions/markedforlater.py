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
        images = shared.images()

        shared.ao3_login(repo, fileops, True)

        link = shared.marked_for_later_link(fileops)
        visited = shared.visited(fileops, filetypes)

        print(strings.AO3_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, filetypes, 0, series, images, True)
        ao3.download(link, visited)


def gui_action(metadata):
    fileops = FileOps()
    filetypes, filetype_handler = shared_gui.download_types(fileops)
    images, images_handler = shared_gui.images()
    series, series_handler = shared_gui.series()

    def handler(event, values, window):
        filetype_handler(event, values, window)
        images_handler(event, values, window)
        series_handler(event, values, window)
        if event == 'OK':
            with Repository() as repo:
                fileops = FileOps()

                shared_gui.handle_login(window.metadata, repo, force = True)

                link = shared.marked_for_later_link(fileops)
                visited = shared.visited(fileops, window.metadata['filetypes'])

                print(strings.AO3_INFO_DOWNLOADING)

                ao3 = Ao3(repo, fileops, window.metadata['filetypes'], 0, window.metadata['series'], window.metadata['images'], True)
                ao3.download(link, visited)

    layout = [filetypes, 
              images,
              series, 
              [shared_gui.output()],
              [sg.OK(), shared_gui.back()]]
    window = sg.Window("Download marked for later", layout, metadata=metadata, finalize=True)
    return window, handler