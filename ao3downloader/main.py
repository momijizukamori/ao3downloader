import ao3downloader.strings as strings

import ao3downloader.actions.ao3download as ao3download
import ao3downloader.actions.pinboarddownload as pinboarddownload
import ao3downloader.actions.updatefics as updatefics
import ao3downloader.actions.redownload as redownload
import ao3downloader.actions.logvisualization as logvisualization
import ao3downloader.actions.updateseries as updateseries


def ao3_download_action():
    ao3download.action()


def update_epubs_action():
    updatefics.action()


def update_series_action():
    updateseries.action()
    

def re_download_action():
    redownload.action()


def pinboard_download_action():
    pinboarddownload.action()


def log_visualization_action():
    logvisualization.action()


def display_menu():
    print(strings.PROMPT_OPTIONS)
    for key, value in actions.items():
        try:
            desc = value.description
        except AttributeError:
            desc = value.__name__
        print(' {}: {}'.format(key, desc))


def choose(choice):
    try:
        function = actions[choice]
        try:
            function()
        except Exception as e:
            print(str(e))
    except KeyError as e:
        print(strings.PROMPT_INVALID_ACTION)


display_menu.description = strings.ACTION_DESCRIPTION_DISPLAY_MENU
ao3_download_action.description = strings.ACTION_DESCRIPTION_AO3
update_epubs_action.description = strings.ACTION_DESCRIPTION_UPDATE
pinboard_download_action.description = strings.ACTION_DESCRIPTION_PINBOARD
log_visualization_action.description = strings.ACTION_DESCRIPTION_VISUALIZATION
re_download_action.description = strings.ACTION_DESCRIPTION_REDOWNLOAD
update_series_action.description = strings.ACTION_DESCRIPTION_UPDATE_SERIES

QUIT_ACTION = 'q'
MENU_ACTION = 'd'

actions = {
    MENU_ACTION: display_menu,
    'a': ao3_download_action,
    'u': update_epubs_action,
    's': update_series_action,
    'r': re_download_action,
    'p': pinboard_download_action,
    'v': log_visualization_action
    }

def main():
    display_menu()

    while True:
        print('\'{}\' to display the menu again'.format(MENU_ACTION))
        print('please enter your choice, or \'{}\' to quit:'.format(QUIT_ACTION))
        choice = input()
        if choice == QUIT_ACTION: break
        choose(choice)

if __name__ == 'main':
    main()