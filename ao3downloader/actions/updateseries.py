import traceback

from ao3downloader import parse_text, strings, update
from ao3downloader.actions.shared import get_files_of_type
from ao3downloader.actions.BaseAction import BaseAction
from ao3downloader.ao3 import Ao3
from ao3downloader.repo import Repository
from tqdm import tqdm


class UpdateSeriesAction:
    def action(self: BaseAction):
        with Repository() as repo:
            folder = self.update_folder()
            update_filetypes = self.update_types()
            download_filetypes = self.download_types()
            images = self.images()

            self.ao3_login(repo)

            files = get_files_of_type(folder, update_filetypes, self.log)

            self.log(strings.SERIES_INFO_FILES)

            works = []
            for file in tqdm(files):
                try:
                    work = update.process_file(file['path'], file['filetype'], True, True)
                    if work:
                        works.append(work)
                        self.fileops.write_log({'message': strings.MESSAGE_SERIES_FILE, 'path': file['path'], 'link': work['link'], 'series': work['series']})
                except Exception as e:
                    self.fileops.write_log({'message': strings.ERROR_FIC_IN_SERIES, 'path': file['path'], 'error': str(e), 'stacktrace': traceback.format_exc()})    

            self.log(strings.SERIES_INFO_URLS)

            series = dict[str, list[str]]()
            for work in works:
                for s in work['series']:
                    if s not in series:
                        series[s] = []
                    link = work['link'].replace('http://', 'https://')
                    if link not in series[s]:
                        series[s].append(link)

            logs = self.fileops.load_logfile()
            if logs:
                unsuccessful = parse_text.get_unsuccessful_downloads(logs)
                if any('/series/' in x for x in unsuccessful):
                    self.log(strings.SERIES_INFO_FILTER)
                    series = {k: v for k, v in series.items() if k not in unsuccessful}

            self.log(strings.SERIES_INFO_NUM.format(len(series)))

            self.log(strings.SERIES_INFO_DOWNLOADING)

            ao3 = Ao3(repo, self.fileops, download_filetypes, None, True, images, output = self.log)

            self.progress(lambda key, value: ao3.update_series(key, value), series.items())
