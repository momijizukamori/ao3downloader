from ao3downloader import parse_text, parse_xml, strings
from ao3downloader.actions.base import shared
from ao3downloader.actions.base.BaseAction import BaseAction
from ao3downloader.ao3 import Ao3
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository
from tqdm import tqdm

class PinboardDownloadAction(BaseAction):
    def action(self):
        with Repository() as repo:
            filetypes = self.download_types()
            date = self.pinboard_date()
            exclude_toread = self.pinboard_exclude()
            images = self.images()
            api_token = shared.api_token(self.fileops)
            
            self.ao3_login(repo)
            
            self.log(strings.PINBOARD_INFO_GETTING_BOOKMARKS)

            url = parse_text.get_pinboard_url(api_token, date)
            bookmark_xml = repo.get_xml(url)
            bookmarks = parse_xml.get_bookmark_list(bookmark_xml, exclude_toread)

            self.log(strings.PINBOARD_INFO_NUM_RETURNED.format(len(bookmarks)))

            logs = self.fileops.load_logfile()
            if logs:
                self.log(strings.INFO_EXCLUDING_WORKS)
                titles = parse_text.get_title_dict(logs)
                unsuccessful = parse_text.get_unsuccessful_downloads(logs)
                bookmarks = list(filter(lambda x: 
                    not self.fileops.file_exists(x['href'], titles, filetypes) 
                    and x['href'] not in unsuccessful, 
                    bookmarks))

            self.log(strings.AO3_INFO_DOWNLOADING)

            ao3 = Ao3(repo, self.fileops, filetypes, None, True, images)

            for item in tqdm(bookmarks):
                ao3.download(item['href'])
