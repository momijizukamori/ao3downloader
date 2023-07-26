from ao3downloader import strings
from ao3downloader.actions.cli.CliAction import CliAction

from ao3downloader.actions.base.ao3download import Ao3DownloadAction
from ao3downloader.actions.base.enterlinks import EnterLinksAction
from ao3downloader.actions.base.getlinks import GetLinksAction
from ao3downloader.actions.base.ignorelist import IgnoreListAction
from ao3downloader.actions.base.logvisualization import LogVisualizationAction
from ao3downloader.actions.base.markedforlater import MarkedForLaterAction
from ao3downloader.actions.base.pinboarddownload import PinboardDownloadAction
from ao3downloader.actions.base.redownload import RedownloadAction
from ao3downloader.actions.base.updatefics import UpdateFicsAction
from ao3downloader.actions.base.updateseries import UpdateSeriesAction


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
