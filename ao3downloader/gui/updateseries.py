import traceback

from ao3downloader import parse_text, strings, update
from ao3downloader.actions import shared, shared_gui
from ao3downloader.ao3 import Ao3
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository
from tqdm import tqdm
import PySimpleGUI as sg


def action():
    with Repository() as repo:
        fileops = FileOps()

        folder = shared.update_folder(fileops)
        update_filetypes = shared.update_types(fileops)
        download_filetypes = shared.download_types(fileops)
        images = shared.images()

        shared.ao3_login(repo, fileops)

        files = shared.get_files_of_type(folder, update_filetypes)

        print(strings.SERIES_INFO_FILES)

        works = []
        for file in tqdm(files):
            try:
                work = update.process_file(file['path'], file['filetype'], True, True)
                if work:
                    works.append(work)
                    fileops.write_log({'message': strings.MESSAGE_SERIES_FILE, 'path': file['path'], 'link': work['link'], 'series': work['series']})
            except Exception as e:
                fileops.write_log({'message': strings.ERROR_FIC_IN_SERIES, 'path': file['path'], 'error': str(e), 'stacktrace': traceback.format_exc()})    

        print(strings.SERIES_INFO_URLS)

        series = dict[str, list[str]]()
        for work in works:
            for s in work['series']:
                if s not in series:
                    series[s] = []
                link = work['link'].replace('http://', 'https://')
                if link not in series[s]:
                    series[s].append(link)

        logs = fileops.load_logfile()
        if logs:
            unsuccessful = parse_text.get_unsuccessful_downloads(logs)
            if any('/series/' in x for x in unsuccessful):
                print(strings.SERIES_INFO_FILTER)
                series = {k: v for k, v in series.items() if k not in unsuccessful}

        print(strings.SERIES_INFO_NUM.format(len(series)))

        print(strings.SERIES_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, download_filetypes, None, True, images)

        for key, value in tqdm(series.items()):
            ao3.update_series(key, value)

def gui_action(metadata):
    fileops = FileOps()
    layout = []
    handlers = []
    disable_ao3 = not shared_gui.can_login(metadata)
    for widget, handler in [shared_gui.download_types(fileops, "Previously-saved filetypes to check for updates", "update"), shared_gui.download_types(fileops, "New filetypes to download", "download"), shared_gui.images(), shared_gui.ao3_login(disable_ao3)]:
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
                update_filetypes = window.metadata['update_filetypes']
                download_filetypes = window.metadata['download_filetypes']

                shared_gui.handle_login(window.metadata, repo)


                files = shared.get_files_of_type(path, update_filetypes)

                print(strings.SERIES_INFO_FILES)

                works = []
                for file in tqdm(files):
                    try:
                        work = update.process_file(file['path'], file['filetype'], True, True)
                        if work:
                            works.append(work)
                            fileops.write_log({'message': strings.MESSAGE_SERIES_FILE, 'path': file['path'], 'link': work['link'], 'series': work['series']})
                    except Exception as e:
                        fileops.write_log({'message': strings.ERROR_FIC_IN_SERIES, 'path': file['path'], 'error': str(e), 'stacktrace': traceback.format_exc()})    

                print(strings.SERIES_INFO_URLS)

                series = dict[str, list[str]]()
                for work in works:
                    for s in work['series']:
                        if s not in series:
                            series[s] = []
                        link = work['link'].replace('http://', 'https://')
                        if link not in series[s]:
                            series[s].append(link)

                logs = fileops.load_logfile()
                if logs:
                    unsuccessful = parse_text.get_unsuccessful_downloads(logs)
                    if any('/series/' in x for x in unsuccessful):
                        print(strings.SERIES_INFO_FILTER)
                        series = {k: v for k, v in series.items() if k not in unsuccessful}

                print(strings.SERIES_INFO_NUM.format(len(series)))

                print(strings.SERIES_INFO_DOWNLOADING)

                ao3 = Ao3(repo, fileops, download_filetypes, None, True, window.metadata['images'])

                for key, value in tqdm(series.items()):
                    ao3.update_series(key, value)

    layout = layout + [
              [sg.Text(strings.REDOWNLOAD_PROMPT_FOLDER)],
              [sg.Input(key="path", enable_events=True), sg.FolderBrowse()],
              [shared_gui.output()],
              [sg.OK(disabled=True), shared_gui.back()]]
    window = sg.Window("Update series", layout, metadata=metadata, finalize=True)
    return window, enterlinks_handler