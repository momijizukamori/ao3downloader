import PySimpleGUI as sg
import ao3downloader.strings as strings

from ao3downloader.fileio import FileOps

from ao3downloader.gui.enterlinks import EnterLinksGuiAction
from ao3downloader.gui.GuiAction import GuiAction
# from ao3downloader.actions import pinboarddownload
# from ao3downloader.actions import updatefics
# from ao3downloader.actions import redownload
# from ao3downloader.actions import logvisualization
# from ao3downloader.actions import updateseries
# from ao3downloader.actions import getlinks
# from ao3downloader.actions import markedforlater
# from ao3downloader.actions import enterlinks
# from ao3downloader.actions import ignorelist
# from ao3downloader.actions import creds


QUIT_ACTION = 'q'
MENU_ACTION = 'd'

ACTIONS = [
    # Ao3DownloadCliAction(),
    # PinboardDownloadCliAction(),
    # UpdateFicsCliAction(),
    # RedownloadCliAction(),
    # LogVisualizationCliAction(),
    # UpdateSeriesCliAction(),
    # GetLinksCliAction(),
    # MarkedForLaterCliAction(),
    EnterLinksGuiAction,
    # IgnoreListCliAction(),
    ]

ACTIONS_MAP = {
}
for action in ACTIONS:
    ACTIONS_MAP[action.key] = action



def display_window():
    fileops = FileOps()
    settings = fileops.get_settings_json()
    layout = []
    for action in ACTIONS:
        layout.append([sg.Button(action.desc, k=action.key, expand_x = True)])
    layout.append([sg.HorizontalSeparator()])
    layout.append([sg.Push(), sg.Button('Quit', k='q')])
    return sg.Window('Ao3 Downloader', layout, metadata=settings)


# ao3_download_action.description = strings.ACTION_DESCRIPTION_AO3
# update_epubs_action.description = strings.ACTION_DESCRIPTION_UPDATE
# pinboard_download_action.description = strings.ACTION_DESCRIPTION_PINBOARD
# log_visualization_action.description = strings.ACTION_DESCRIPTION_VISUALIZATION
# re_download_action.description = strings.ACTION_DESCRIPTION_REDOWNLOAD
# update_series_action.description = strings.ACTION_DESCRIPTION_UPDATE_SERIES
# links_only_action.description = strings.ACTION_DESCRIPTION_LINKS_ONLY
# marked_for_later_action.description = strings.ACTION_DESCRIPTION_MARKED_FOR_LATER
# file_input_action.description = strings.ACTION_DESCRIPTION_FILE_INPUT
# ignorelist_action.description = strings.ACTION_DESCRIPTION_CONFIGURE_IGNORELIST
# creds_action.description = "Configure credentials"

QUIT_ACTION = 'q'

# actions = {
#     'c': creds_action,
#     'a': ao3_download_action,
#     'l': links_only_action,
#     'f': file_input_action,
#     'u': update_epubs_action,
#     's': update_series_action,
#     'r': re_download_action,
#     'm': marked_for_later_action,
#     # 'p': pinboard_download_action,
#     # 'v': log_visualization_action,
#     'i': ignorelist_action
#     }

sg.theme('Gray Gray Gray')
window = display_window()
current_action: GuiAction = None


# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'q':
        break
    if current_action:
        current_action.handle(event, values, window)
    if event == 'Back':
        window.close()
        window = display_window()
        current_action = None
    if event in ACTIONS_MAP.keys():
        window.close()
        action_cls = ACTIONS_MAP[event]
        current_action = action_cls(window.metadata)
        window = current_action.render()



# Finish up by removing from the screen
window.close()
