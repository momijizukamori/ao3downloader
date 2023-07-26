import ao3downloader.strings as strings

from ao3downloader.actions.cli import Ao3DownloadCliAction
from ao3downloader.actions.cli import PinboardDownloadCliAction
from ao3downloader.actions.cli import UpdateFicsCliAction
from ao3downloader.actions.cli import RedownloadCliAction
from ao3downloader.actions.cli import LogVisualizationCliAction
from ao3downloader.actions.cli import UpdateSeriesCliAction
from ao3downloader.actions.cli import GetLinksCliAction
from ao3downloader.actions.cli import MarkedForLaterCliAction
from ao3downloader.actions.cli import EnterLinksCliAction
from ao3downloader.actions.cli import IgnoreListCliAction

QUIT_ACTION = 'q'
MENU_ACTION = 'd'

ACTIONS = [
    Ao3DownloadCliAction(),
    PinboardDownloadCliAction(),
    UpdateFicsCliAction(),
    RedownloadCliAction(),
    LogVisualizationCliAction(),
    UpdateSeriesCliAction(),
    GetLinksCliAction(),
    MarkedForLaterCliAction(),
    EnterLinksCliAction(),
    IgnoreListCliAction(),
    ]


def display_menu():
    print(strings.PROMPT_OPTIONS)
    print(f' {MENU_ACTION}: {strings.ACTION_DESCRIPTION_DISPLAY_MENU}')
    for action in ACTIONS:
        print(f' {action.key}: {action.desc}')

ACTIONS_MAP = {
    MENU_ACTION: display_menu,
}
for action in ACTIONS:
    ACTIONS_MAP[action.key] = action.action


def choose(choice):
    try:
        function = ACTIONS_MAP[choice]
        try:
            function()
        except Exception as e:
            print(str(e))
    except KeyError as e:
        print(strings.PROMPT_INVALID_ACTION)

display_menu()

while True:
    print('\'{}\' to display the menu again'.format(MENU_ACTION))
    print('please enter your choice, or \'{}\' to quit:'.format(QUIT_ACTION))
    choice = input()
    if choice == QUIT_ACTION: break
    choose(choice)
