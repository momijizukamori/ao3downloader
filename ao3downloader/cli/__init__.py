from ao3downloader import strings
from ao3downloader.cli.CliAction import CliAction

from ao3downloader.actions.ao3download import Ao3DownloadAction
from ao3downloader.actions.enterlinks import EnterLinksAction
from ao3downloader.actions.getlinks import GetLinksAction
from ao3downloader.actions.ignorelist import IgnoreListAction
from ao3downloader.actions.logvisualization import LogVisualizationAction
from ao3downloader.actions.markedforlater import MarkedForLaterAction
from ao3downloader.actions.pinboarddownload import PinboardDownloadAction
from ao3downloader.actions.redownload import RedownloadAction
from ao3downloader.actions.updatefics import UpdateFicsAction
from ao3downloader.actions.updateseries import UpdateSeriesAction


class Ao3DownloadCliAction(CliAction, Ao3DownloadAction):
    key = 'a'
    desc = strings.ACTION_DESCRIPTION_AO3


class EnterLinksCliAction(CliAction, EnterLinksAction):
    key = 'f'
    desc = strings.ACTION_DESCRIPTION_FILE_INPUT


class GetLinksCliAction(CliAction, GetLinksAction):
    key = 'l'
    desc = strings.ACTION_DESCRIPTION_LINKS_ONLY


class IgnoreListCliAction(CliAction, IgnoreListAction):
    key = 'i'
    desc = strings.ACTION_DESCRIPTION_CONFIGURE_IGNORELIST


class LogVisualizationCliAction(CliAction, LogVisualizationAction):
    key = 'v'
    desc = strings.ACTION_DESCRIPTION_VISUALIZATION


class MarkedForLaterCliAction(CliAction, MarkedForLaterAction):
    key = 'm'
    desc = strings.ACTION_DESCRIPTION_MARKED_FOR_LATER


class PinboardDownloadCliAction(CliAction, PinboardDownloadAction):
    key = 'p'
    desc = strings.ACTION_DESCRIPTION_PINBOARD


class RedownloadCliAction(CliAction, RedownloadAction):
    key = 'r'
    desc = strings.ACTION_DESCRIPTION_REDOWNLOAD


class UpdateFicsCliAction(CliAction, UpdateFicsAction):
    key = 'u'
    desc = strings.ACTION_DESCRIPTION_UPDATE


class UpdateSeriesCliAction(CliAction, UpdateSeriesAction):
    key = 's'
    desc = strings.ACTION_DESCRIPTION_UPDATE_SERIES
