from ao3downloader.fileio import FileOps
from ao3downloader.repo import Repository

class BaseAction:
    def __init__(self):
        self.fileops = FileOps()

    @staticmethod
    def log(text: str) -> None:
        print(text)

    @staticmethod
    def pages() -> int:
        return 0
    
    @staticmethod
    def link() -> str:
        return ''
  
    @staticmethod
    def images():
        return False
    
    @staticmethod
    def series():
        return False
    
    @staticmethod
    def metadata():
        return False
    
    @staticmethod
    def ignorelist_check_deleted():
        return False
    
    @staticmethod
    def pinboard_exclude() -> bool:
        return False
    
    @staticmethod
    def redownload_oldtypes() -> list[str]:
        return []
    
    @staticmethod
    def redownload_newtypes() -> list[str]:
        return []
    
    @staticmethod
    def download_types() -> list[str]:
        return []
    
    @staticmethod
    def update_types() -> list[str]:
        return []

    @staticmethod
    def update_folder() -> str:
        return ''

    @staticmethod
    def pinboard_date():
        return None
    
    @staticmethod
    def redownload_folder() -> str:
        return ''
    
    @staticmethod
    def update_folder() -> str:
        return ''
    
    @staticmethod
    def ao3_login(repo: Repository, force: bool = False):
        pass