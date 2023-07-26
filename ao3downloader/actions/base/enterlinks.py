from ao3downloader import strings
from ao3downloader.actions.base import shared
from ao3downloader.actions.base.BaseAction import BaseAction
from ao3downloader.ao3 import Ao3
from ao3downloader.repo import Repository

from tqdm import tqdm

class EnterLinksAction(BaseAction):
    def action(self):
        with Repository() as repo:
            filetypes = self.download_types()
            images = self.images()

            self.log(strings.AO3_PROMPT_FILE_INPUT)
            path = input()
            with open(path) as f:
                links = f.readlines()

            self.ao3_login(repo, self.fileops)

            visited = shared.visited(self.fileops, filetypes)

            self.log(strings.AO3_INFO_DOWNLOADING)

            ao3 = Ao3(repo, self.fileops, filetypes, 0, True, images)
            for link in tqdm(links):
                ao3.download(link.strip(), visited)
