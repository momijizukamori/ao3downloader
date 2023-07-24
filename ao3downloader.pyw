import PySimpleGUI as sg
import ao3downloader.strings as strings

from ao3downloader.fileio import FileOps

from ao3downloader.actions import ao3download
from ao3downloader.actions import pinboarddownload
from ao3downloader.actions import updatefics
from ao3downloader.actions import redownload
from ao3downloader.actions import logvisualization
from ao3downloader.actions import updateseries
from ao3downloader.actions import getlinks
from ao3downloader.actions import markedforlater
from ao3downloader.actions import enterlinks
from ao3downloader.actions import ignorelist
from ao3downloader.actions import creds


def ao3_download_action(metadata):
    return ao3download.gui_action(metadata)


def links_only_action(metadata):
    return getlinks.gui_action(metadata)


def file_input_action(metadata):
    return enterlinks.gui_action(metadata)


def update_epubs_action(metadata):
    return updatefics.gui_action(metadata)


def update_series_action(metadata):
    return updateseries.gui_action(metadata)
    

def re_download_action(metadata):
    return redownload.gui_action(metadata)


def marked_for_later_action(metadata):
    return markedforlater.gui_action(metadata)


def pinboard_download_action():
    pinboarddownload.action()


def log_visualization_action():
    logvisualization.action()


def ignorelist_action(metadata):
    return ignorelist.gui_action(metadata)

def creds_action(metadata):
    return creds.gui_action(metadata)



def display_window():
    fileops = FileOps()
    settings = fileops.get_settings_json()
    layout = []
    for key, value in actions.items():
        layout.append([sg.Button(value.description, k=key, expand_x = True)])
    layout.append([sg.HorizontalSeparator()])
    layout.append([sg.Push(), sg.Button('Quit', k='q')])
    return sg.Window('Ao3 Downloader', layout, metadata=settings), []


ao3_download_action.description = strings.ACTION_DESCRIPTION_AO3
update_epubs_action.description = strings.ACTION_DESCRIPTION_UPDATE
pinboard_download_action.description = strings.ACTION_DESCRIPTION_PINBOARD
log_visualization_action.description = strings.ACTION_DESCRIPTION_VISUALIZATION
re_download_action.description = strings.ACTION_DESCRIPTION_REDOWNLOAD
update_series_action.description = strings.ACTION_DESCRIPTION_UPDATE_SERIES
links_only_action.description = strings.ACTION_DESCRIPTION_LINKS_ONLY
marked_for_later_action.description = strings.ACTION_DESCRIPTION_MARKED_FOR_LATER
file_input_action.description = strings.ACTION_DESCRIPTION_FILE_INPUT
ignorelist_action.description = strings.ACTION_DESCRIPTION_CONFIGURE_IGNORELIST
creds_action.description = "Configure credentials"

QUIT_ACTION = 'q'

actions = {
    'c': creds_action,
    'a': ao3_download_action,
    'l': links_only_action,
    'f': file_input_action,
    'u': update_epubs_action,
    's': update_series_action,
    'r': re_download_action,
    'm': marked_for_later_action,
    # 'p': pinboard_download_action,
    # 'v': log_visualization_action,
    'i': ignorelist_action
    }

sg.theme('Gray Gray Gray')
window, handlers = display_window()


# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'q':
        break
    for fn in handlers:
        fn(event, values, window)
    if event == 'Back':
        window.close()
        window, handlers = display_window()
    if event in actions.keys():
        window.close()
        window, handle_fn = actions[event](window.metadata)
        handlers.append(handle_fn)


# Finish up by removing from the screen
window.close()
