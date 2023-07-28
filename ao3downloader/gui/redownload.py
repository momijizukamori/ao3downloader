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
        
        folder = shared.redownload_folder()
        oldtypes = shared.redownload_oldtypes()
        newtypes = shared.redownload_newtypes()
        images = shared.images()

        shared.ao3_login(repo, fileops)

        fics = shared.get_files_of_type(folder, oldtypes)

        print(strings.REDOWNLOAD_INFO_URLS)

        works = []
        for fic in tqdm(fics):
            try:
                work = update.process_file(fic['path'], fic['filetype'], False)
                if work: 
                    works.append(work)
                    fileops.write_log({'message': strings.MESSAGE_FIC_FILE, 'path': fic['path'], 'link': work['link']})
            except Exception as e:
                fileops.write_log({'message': strings.ERROR_REDOWNLOAD, 'path': fic['path'], 'error': str(e), 'stacktrace': traceback.format_exc()})

        urls = list(set(map(lambda x: x['link'], works)))

        print(strings.REDOWNLOAD_INFO_DONE.format(len(urls)))

        logs = fileops.load_logfile()
        if logs:
            print(strings.INFO_EXCLUDING_WORKS)
            titles = parse_text.get_title_dict(logs)
            unsuccessful = parse_text.get_unsuccessful_downloads(logs)
            urls = list(filter(lambda x: 
                not fileops.file_exists(x, titles, newtypes)
                and x not in unsuccessful,
                urls))

        print(strings.AO3_INFO_DOWNLOADING)

        ao3 = Ao3(repo, fileops, newtypes, None, False, images)

        for url in tqdm(urls):
            ao3.download(url)

def gui_action(metadata):
    fileops = FileOps()
    layout = []
    handlers = []
    disable_ao3 = not shared_gui.can_login(metadata)
    for widget, handler in [shared_gui.download_types(fileops, "Previously-saved filetypes to redownload", "old"), shared_gui.download_types(fileops, "New filetypes to download", "new"), shared_gui.images(), shared_gui.ao3_login(disable_ao3)]:
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
                oldtypes = window.metadata['old_filetypes']
                newtypes = window.metadata['new_filetypes']

                shared_gui.handle_login(window.metadata, repo)

                fics = shared.get_files_of_type(path, oldtypes)

                print(strings.REDOWNLOAD_INFO_URLS)

                works = []
                for fic in tqdm(fics):
                    try:
                        work = update.process_file(fic['path'], fic['filetype'], False)
                        if work: 
                            works.append(work)
                            fileops.write_log({'message': strings.MESSAGE_FIC_FILE, 'path': fic['path'], 'link': work['link']})
                    except Exception as e:
                        fileops.write_log({'message': strings.ERROR_REDOWNLOAD, 'path': fic['path'], 'error': str(e), 'stacktrace': traceback.format_exc()})

                urls = list(set(map(lambda x: x['link'], works)))

                print(strings.REDOWNLOAD_INFO_DONE.format(len(urls)))

                logs = fileops.load_logfile()
                if logs:
                    print(strings.INFO_EXCLUDING_WORKS)
                    titles = parse_text.get_title_dict(logs)
                    unsuccessful = parse_text.get_unsuccessful_downloads(logs)
                    urls = list(filter(lambda x: 
                        not fileops.file_exists(x, titles, newtypes)
                        and x not in unsuccessful,
                        urls))

                print(strings.AO3_INFO_DOWNLOADING)

                ao3 = Ao3(repo, fileops, newtypes, None, False, window.metadata['images'])

                for url in tqdm(urls):
                    ao3.download(url)

    layout = layout + [
              [sg.Text(strings.REDOWNLOAD_PROMPT_FOLDER)],
              [sg.Input(key="path", enable_events=True), sg.FolderBrowse()],
              [shared_gui.output()],
              [sg.OK(disabled=True), shared_gui.back()]]
    window = sg.Window("Redownload fics", layout, metadata=metadata, finalize=True)
    return window, enterlinks_handler