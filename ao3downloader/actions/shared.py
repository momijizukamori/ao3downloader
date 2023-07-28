import os

from ao3downloader import parse_text, strings
from ao3downloader.fileio import FileOps

def visited(fileops: FileOps, filetypes: list[str], log: callable = print) -> list[str]:
    visited = []
    logs = fileops.load_logfile()
    if logs:
        log(strings.AO3_INFO_VISITED)
        titles = parse_text.get_title_dict(logs)
        visited = list({x for x in titles if 
            fileops.file_exists(x, titles, filetypes)})
    if os.path.exists(strings.IGNORELIST_FILE_NAME):
        with open(strings.IGNORELIST_FILE_NAME, 'r', encoding='utf-8') as f: 
                visited.extend([x[:x.find('; ')] for x in f.readlines()])
    return visited


def api_token(fileops: FileOps) -> str:
    return fileops.setting(
            strings.PINBOARD_PROMPT_API_TOKEN, 
            strings.SETTING_API_TOKEN)

def marked_for_later_link(fileops: FileOps) -> str:
    username = fileops.get_setting(strings.SETTING_USERNAME)
    return f'{strings.AO3_BASE_URL}/users/{username}/readings?show=to-read'


def get_files_of_type(folder: str, filetypes: list[str], log: callable = print) -> list[dict[str, str]]:
    log(strings.UPDATE_INFO_FILES)
    results = []
    for subdir, dirs, files in os.walk(folder):
        for file in files:
            filetype = os.path.splitext(file)[1].upper()[1:]
            if filetype in filetypes:
                path = os.path.join(subdir, file)
                results.append({'path': path, 'filetype': filetype})
    log(strings.UPDATE_INFO_NUM_RETURNED.format(len(results)))
    return results
