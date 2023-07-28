from ao3downloader import strings
from ao3downloader.actions.shared import visited
from ao3downloader.actions.BaseAction import BaseAction
from ao3downloader.ao3 import Ao3
from ao3downloader.repo import Repository

class EnterLinksAction:
    def action(self: BaseAction):
        with Repository() as repo:
            filetypes = self.download_types()
            images = self.images()

            with open(self.file_path()) as f:
                links = f.readlines()

            self.ao3_login(repo, self.fileops)

            visited_list = visited(self.fileops, filetypes, self.log)

            self.log(strings.AO3_INFO_DOWNLOADING)

            ao3 = Ao3(repo, self.fileops, filetypes, 0, True, images, output = self.log)
            self.progress(lambda link: ao3.download(link.strip(), visited_list), links)

