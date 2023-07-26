from ao3downloader import strings
from ao3downloader.actions.base import shared
from ao3downloader.actions.base.BaseAction import BaseAction
from ao3downloader.ao3 import Ao3
from ao3downloader.repo import Repository



class MarkedForLaterAction(BaseAction):
    def action(self):
        with Repository() as repo:

            filetypes = self.download_types()
            series = self.series()
            images = self.images()

            self.ao3_login(repo, True)

            link = shared.marked_for_later_link(self.fileops)
            visited = shared.visited(self.fileops, filetypes)

            self.log(strings.AO3_INFO_DOWNLOADING)

            ao3 = Ao3(repo, self.fileops, filetypes, 0, series, images, True)
            ao3.download(link, visited)
