import itertools
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

        fics = shared.get_files_of_type(folder, update_filetypes)

        print(strings.UPDATE_INFO_URLS)

        works = []
        for fic in tqdm(fics):
            try:
                work = update.process_file(fic['path'], fic['filetype'])
                if work:
                    works.append(work)
                    fileops.write_log({'message': strings.MESSAGE_INCOMPLETE_FIC, 'path': fic['path'], 'link': work['link']})
            except Exception as e:
                fileops.write_log({'message': strings.ERROR_INCOMPLETE_FIC, 'path': fic['path'], 'error': str(e), 'stacktrace': traceback.format_exc()})    

        # remove duplicate work links. take lowest number of chapters.
        works_cleaned = []
        works_sorted = sorted(works, key=lambda x: x['link'])
        for link, group in itertools.groupby(works_sorted, lambda x: x['link']):
            chapters = min(group, key=lambda x: x['chapters'])['chapters']
            works_cleaned.append({'link': link, 'chapters': chapters})

        print(strings.UPDATE_INFO_URLS_DONE)

        logs = fileops.load_logfile()
        if logs:
            unsuccessful = parse_text.get_unsuccessful_downloads(logs)
            if any('/works/' in x for x in unsuccessful):
                print(strings.UPDATE_INFO_FILTER)
                works_cleaned = list(filter(lambda x: x['link'] not in unsuccessful, works_cleaned))

        print(strings.UPDATE_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, download_filetypes, None, False, images)

        for work in tqdm(works_cleaned):
            ao3.update(work['link'], work['chapters'])

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

                fics = shared.get_files_of_type(path, update_filetypes)

                print(strings.UPDATE_INFO_URLS)

                works = []
                for fic in tqdm(fics):
                    try:
                        work = update.process_file(fic['path'], fic['filetype'])
                        if work:
                            works.append(work)
                            fileops.write_log({'message': strings.MESSAGE_INCOMPLETE_FIC, 'path': fic['path'], 'link': work['link']})
                    except Exception as e:
                        fileops.write_log({'message': strings.ERROR_INCOMPLETE_FIC, 'path': fic['path'], 'error': str(e), 'stacktrace': traceback.format_exc()})    

                # remove duplicate work links. take lowest number of chapters.
                works_cleaned = []
                works_sorted = sorted(works, key=lambda x: x['link'])
                for link, group in itertools.groupby(works_sorted, lambda x: x['link']):
                    chapters = min(group, key=lambda x: x['chapters'])['chapters']
                    works_cleaned.append({'link': link, 'chapters': chapters})

                print(strings.UPDATE_INFO_URLS_DONE)

                logs = fileops.load_logfile()
                if logs:
                    unsuccessful = parse_text.get_unsuccessful_downloads(logs)
                    if any('/works/' in x for x in unsuccessful):
                        print(strings.UPDATE_INFO_FILTER)
                        works_cleaned = list(filter(lambda x: x['link'] not in unsuccessful, works_cleaned))

                print(strings.UPDATE_INFO_DOWNLOADING)

                ao3 = Ao3(repo, fileops, download_filetypes, None, False, window.metadata['images'])

                for work in tqdm(works_cleaned):
                    ao3.update(work['link'], work['chapters'])

    layout = layout + [
              [sg.Text(strings.REDOWNLOAD_PROMPT_FOLDER)],
              [sg.Input(key="path", enable_events=True), sg.FolderBrowse()],
              [shared_gui.output()],
              [sg.OK(disabled=True), shared_gui.back()]]
    window = sg.Window("Update fics", layout, metadata=metadata, finalize=True)
    return window, enterlinks_handler