import csv
import datetime
import os

from ao3downloader import strings
from ao3downloader.actions.base import shared
from ao3downloader.actions.base.BaseAction import BaseAction
from ao3downloader.ao3 import Ao3
from ao3downloader.repo import Repository

class GetLinksAction(BaseAction):
    def action(self):
        with Repository() as repo:

            link = self.link()
            series = self.series()
            pages = self.pages()
            metatdata = self.metadata()

            self.ao3_login(repo, self.fileops)

            ao3 = Ao3(repo, self.fileops, None, pages, series, False)
            links = ao3.get_work_links(link, metatdata)

            if metatdata:
                flattened = [self.flatten_dict(k, v) for k, v in links.items()]
                filename = f'links_{datetime.datetime.now().strftime("%m%d%Y%H%M%S")}.csv'
                with open(os.path.join(strings.DOWNLOAD_FOLDER_NAME, filename), 'w', newline='', encoding='utf-8') as f:
                    keys = []
                    sample = flattened[0]
                    for key in sample: keys.append(key)
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    for item in flattened:
                        writer.writerow(item)
            else:
                filename = f'links_{datetime.datetime.now().strftime("%m%d%Y%H%M%S")}.txt'
                with open(os.path.join(strings.DOWNLOAD_FOLDER_NAME, filename), 'w') as f:
                    for l in links:
                        f.write(l + '\n')


    @staticmethod
    def flatten_dict(k: str, v: dict) -> dict:
        v['link'] = k
        return v