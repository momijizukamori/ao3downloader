from typing import Callable, Iterator
from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository
from ao3downloader.actions.BaseAction import BaseAction
from ao3downloader import exceptions, strings
import datetime
import os
from tqdm import tqdm

class CliAction(BaseAction):
    def __init__(self) -> None:
        self.fileops = FileOps()
    
    def log(self, text: str):
        print(text)


    def ao3_login(self, repo: Repository, force: bool=False) -> None:
        if force:
            login = True
        else:
            self.log(strings.AO3_PROMPT_LOGIN)
            login = False if input() == strings.PROMPT_NO else True

        if login:
            username = self.fileops.setting(
                strings.AO3_PROMPT_USERNAME,
                strings.SETTING_USERNAME)
            password = self.fileops.setting(
                strings.AO3_PROMPT_PASSWORD,
                strings.SETTING_PASSWORD)

            self.log(strings.AO3_INFO_LOGIN)
            try:
                repo.login(username, password)
            except exceptions.LoginException:
                self.fileops.save_setting(strings.SETTING_USERNAME, None)
                self.fileops.save_setting(strings.SETTING_PASSWORD, None)
                raise

    def bool_prompt(self, prompt_text: str) -> bool:
        self.log(prompt_text)
        return True if input() == strings.PROMPT_YES else False
    
    def images(self) -> bool:
        return self.bool_prompt(strings.AO3_PROMPT_IMAGES)
    
    def series(self) -> bool:
        return self.bool_prompt(strings.AO3_PROMPT_SERIES)
    
    def metadata(self) -> bool:
        return self.bool_prompt(strings.AO3_PROMPT_METADATA)
        
    def ignorelist_check_deleted(self) -> bool:
        return self.bool_prompt(strings.IGNORELIST_PROMPT_CHECK_DELETED)
    
    def pinboard_exclude(self) -> bool:
        return self.bool_prompt(strings.PINBOARD_PROMPT_INCLUDE_UNREAD)


    def redownload_oldtypes(self) -> list[str]:
        oldtypes = []
        while True:
            filetype = ''
            while filetype not in strings.UPDATE_ACCEPTABLE_FILE_TYPES:
                self.log(strings.REDOWNLOAD_PROMPT_FILE_TYPE)
                filetype = input()
            oldtypes.append(filetype)
            self.log(strings.REDOWNLOAD_INFO_FILE_TYPE.format(filetype))
            self.log(strings.AO3_PROMPT_DOWNLOAD_TYPES_COMPLETE)
            if input() == strings.PROMPT_YES:
                oldtypes = list(set(oldtypes))
                break
        return oldtypes


    def redownload_newtypes(self) -> list[str]:
        newtypes = []
        while True:
            filetype = ''
            while filetype not in strings.AO3_ACCEPTABLE_DOWNLOAD_TYPES:
                self.log(strings.AO3_PROMPT_DOWNLOAD_TYPE)
                filetype = input()
            newtypes.append(filetype)
            self.log(strings.AO3_INFO_FILE_TYPE.format(filetype))
            self.log(strings.AO3_PROMPT_DOWNLOAD_TYPES_COMPLETE)
            if input() == strings.PROMPT_YES:
                newtypes = list(set(newtypes))
                break
        return newtypes

    def link(self) -> str:
        link = self.get_last_page_downloaded()
        if not link: 
            self.log(strings.AO3_PROMPT_LINK)
            link = input()
        return link


    def pages(self) -> int:
        self.log(strings.AO3_PROMPT_PAGES)
        pages = input()

        try:
            pages = int(pages)
            if pages <= 0:
                pages = None
        except:
            pages = None

        return pages

    def pinboard_date(self) -> datetime.datetime:
        self.log(strings.PINBOARD_PROMPT_DATE)
        getdate = True if input() == strings.PROMPT_YES else False
        if getdate:
            date_format = 'mm/dd/yyyy'
            self.log(strings.PINBOARD_PROMPT_ENTER_DATE.format(date_format))
            inputdate = input()
            date = datetime.strptime(inputdate, '%m/%d/%Y')
        else:
            date = None
        return date

    def get_last_page_downloaded(self, prompt: bool = True) -> str:
        latest = None
        try:
            logs = self.fileops.load_logfile()
            starts = filter(lambda x: 'starting' in x, logs)
            bydate = sorted(starts, key=lambda x: datetime.datetime.strptime(x['timestamp'], '%m/%d/%Y, %H:%M:%S'), reverse=True)
            if bydate: latest = bydate[0]
        except Exception as e:
            self.fileops.write_log({'error': str(e), 'message': strings.ERROR_LOG_FILE, 'stacktrace': traceback.format_exc()})

        link = None
        if latest:
            if prompt:
                self.log(strings.AO3_PROMPT_LAST_PAGE)
                if input() == strings.PROMPT_YES:
                    link = latest['starting']
            else:
                link = latest['starting']

        return link


    def redownload_folder(self) -> str:
        while True:
            self.log(strings.REDOWNLOAD_PROMPT_FOLDER)
            folder = input()
            if os.path.exists(folder): 
                break
            else:
                self.log(strings.INFO_NO_FOLDER)
        return folder

    def update_folder(self) -> str:
        folder = self.fileops.get_setting(strings.SETTING_UPDATE_FOLDER)
        if folder:
            self.log(strings.UPDATE_PROMPT_USE_SAVED_FOLDER)
            if input() == strings.PROMPT_YES: 
                return folder
            else:
                self.fileops.save_setting(
                    strings.SETTING_UPDATE_FOLDER, 
                    None)
        folder = self.fileops.setting(
            strings.UPDATE_PROMPT_INPUT,
            strings.SETTING_UPDATE_FOLDER)
        return folder

    def download_types(self) -> list[str]:
        filetypes = self.fileops.get_setting(strings.SETTING_FILETYPES)
        if isinstance(filetypes, list):
            self.log(strings.AO3_PROMPT_USE_SAVED_DOWNLOAD_TYPES)
            if input() == strings.PROMPT_YES: return filetypes
        filetypes = []
        while(True):
            filetype = ''
            while filetype not in strings.AO3_ACCEPTABLE_DOWNLOAD_TYPES:
                self.log(strings.AO3_PROMPT_DOWNLOAD_TYPE)
                filetype = input()
            filetypes.append(filetype)
            self.log(strings.AO3_INFO_FILE_TYPE.format(filetype))
            self.log(strings.AO3_PROMPT_DOWNLOAD_TYPES_COMPLETE)
            if input() == strings.PROMPT_YES:
                filetypes = list(set(filetypes))
                self.fileops.save_setting(strings.SETTING_FILETYPES, filetypes)
                return filetypes


    def update_types(self) -> list[str]:
        filetypes = self.fileops.get_setting(strings.SETTING_UPDATE_FILETYPES)
        if isinstance(filetypes, list):
            self.log(strings.UPDATE_PROMPT_USE_SAVED_FILE_TYPES)
            if input() == strings.PROMPT_YES: return filetypes
        filetypes = []
        while(True):
            filetype = ''
            while filetype not in strings.UPDATE_ACCEPTABLE_FILE_TYPES:
                self.log(strings.UPDATE_PROMPT_FILE_TYPE)
                filetype = input()
            filetypes.append(filetype)
            self.log(strings.UPDATE_INFO_FILE_TYPE.format(filetype))
            self.log(strings.AO3_PROMPT_DOWNLOAD_TYPES_COMPLETE)
            if input() == strings.PROMPT_YES:
                filetypes = list(set(filetypes))
                self.fileops.save_setting(strings.SETTING_UPDATE_FILETYPES, filetypes)
                return filetypes

    def file_path(self) -> str:
            self.log(strings.AO3_PROMPT_FILE_INPUT)
            path = input()
            return path
    
    def progress(self, callback: Callable[..., any], iterator: Iterator) -> None:
        for i in tqdm(iterator):
            callback(i)