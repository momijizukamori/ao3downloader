import traceback

from ao3downloader import parse_text, strings, update
from ao3downloader.actions.shared import get_files_of_type
from ao3downloader.actions.BaseAction import BaseAction
from ao3downloader.ao3 import Ao3
from ao3downloader.repo import Repository
from tqdm import tqdm


class RedownloadAction:
    def action(self: BaseAction):
        with Repository() as repo:
            
            folder = self.redownload_folder()
            oldtypes = self.redownload_oldtypes()
            newtypes = self.redownload_newtypes()
            images = self.images()

            self.ao3_login(repo)

            fics = get_files_of_type(folder, oldtypes, self.log)

            self.log(strings.REDOWNLOAD_INFO_URLS)

            works = []
            for fic in tqdm(fics):
                try:
                    work = update.process_file(fic['path'], fic['filetype'], False)
                    if work: 
                        works.append(work)
                        self.fileops.write_log({'message': strings.MESSAGE_FIC_FILE, 'path': fic['path'], 'link': work['link']})
                except Exception as e:
                    self.fileops.write_log({'message': strings.ERROR_REDOWNLOAD, 'path': fic['path'], 'error': str(e), 'stacktrace': traceback.format_exc()})

            urls = list(set(map(lambda x: x['link'], works)))

            self.log(strings.REDOWNLOAD_INFO_DONE.format(len(urls)))

            logs = self.fileops.load_logfile()
            if logs:
                self.log(strings.INFO_EXCLUDING_WORKS)
                titles = parse_text.get_title_dict(logs)
                unsuccessful = parse_text.get_unsuccessful_downloads(logs)
                urls = list(filter(lambda x: 
                    not self.fileops.file_exists(x, titles, newtypes)
                    and x not in unsuccessful,
                    urls))

            self.log(strings.AO3_INFO_DOWNLOADING)

            ao3 = Ao3(repo, self.fileops, newtypes, None, False, images, output = self.log)

            for url in tqdm(urls):
                ao3.download(url)
