from ao3downloader import strings
from ao3downloader.actions import shared, shared_gui
from ao3downloader.fileio import FileOps
import PySimpleGUI as sg

def action():
    fileops = FileOps()
    with open(strings.IGNORELIST_FILE_NAME, 'a', encoding='utf-8'): pass
    print(strings.IGNORELIST_INFO_INITIALIZED)
    if shared.ignorelist_check_deleted():
        with open(strings.IGNORELIST_FILE_NAME, 'r', encoding='utf-8') as f: 
            ignorelist = [x[:x.find('; ')] for x in f.readlines()]
        logfile = fileops.load_logfile()
        deleted = [x['link'] for x in logfile if x.get('error') == strings.ERROR_DELETED]
        pathdict = {}
        for d in deleted:
            paths = [x['path'] for x in logfile if 'path' in x and x.get('link') == d or ('series' in x and d in x['series'])]
            if paths: pathdict[d] = list(set(paths))
        newlinks = list(filter(lambda x: x not in ignorelist, deleted))
        with open(strings.IGNORELIST_FILE_NAME, 'a', encoding='utf-8') as f:
            for link in newlinks:
                f.write(f'{link}; Deleted')
                if pathdict[link]: f.write(f': associated filepaths - {pathdict[link]}')
                f.write('\n')


def gui_action(metadata):
    fileops = FileOps()
    with open(strings.IGNORELIST_FILE_NAME, 'a', encoding='utf-8'): pass
    with open(strings.IGNORELIST_FILE_NAME, 'r', encoding='utf-8') as f: 
        ignorelist = f.read()

    layout = [[sg.Text(strings.IGNORELIST_INFO_INITIALIZED_GUI)], 
              [sg.Button("Check logs for deleted scans and add to ignorelist?", key="deleted")],
              [sg.Multiline(ignorelist, key="ignorelist", expand_x=True, size=(50, 15))],
              [sg.Button("Save", key="save"), shared_gui.back()]]
    
    def handler(event, values, window):
        if event == 'deleted':
            with open(strings.IGNORELIST_FILE_NAME, 'r', encoding='utf-8') as f: 
                ignorelist = [x[:x.find('; ')] for x in f.readlines()]
            logfile = fileops.load_logfile()
            deleted = [x['link'] for x in logfile if x.get('error') == strings.ERROR_DELETED]
            pathdict = {}
            for d in deleted:
                paths = [x['path'] for x in logfile if 'path' in x and x.get('link') == d or ('series' in x and d in x['series'])]
                if paths: pathdict[d] = list(set(paths))
            newlinks = list(filter(lambda x: x not in ignorelist, deleted))
            for link in newlinks:
                window['ignorelist'].print(f'{link}; Deleted')
                if pathdict[link]: window['ignorelist'].print(f': associated filepaths - {pathdict[link]}')
                window['ignorelist'].print('\n')
        if event == 'save':
            with open(strings.IGNORELIST_FILE_NAME, 'w', encoding='utf-8') as f:
                f.write(values['ignorelist'])

    window = sg.Window("Update ignorelist", layout, metadata=metadata, finalize=True)
    return window, handler
