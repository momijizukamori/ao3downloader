## What is this?
This is a program intended to help you download fanfiction from the [Archive of Our Own](https://archiveofourown.org/) in bulk. This program is primarily intended to work with links to the Archive of Our Own itself, but has a secondary function of downloading any [Pinboard](https://pinboard.in/) bookmarks that link to the Archive of Our Own. You can ignore the Pinboard functionality if you don't know what Pinboard is or don't use Pinboard.

## Table of Contents

- [Announcements](#announcements): List of changes that may be of note for returning users (not a complete changelog).
- [Instructions](#instructions): Complete instructions for downloading and starting ao3downloader on Windows and Mac (running ao3downloader on Linux is left as an exercise for the reader). I have tried to make this as easy to follow as possible, even for those who have little experience with computers. If any of it is confusing, or you have a suggestion to improve the instructions, please [contact](#questions-comments-bug-reports) me.
- [Menu Options](#menu-options-explanation): Explanation of the options you will see when you start ao3downloader and what they do. Note that most of these options will in turn present you with a series of prompts. These should largely be self-explanatory, however, if you are confused by any of the prompts your question may be answered in the [notes](#notes).
- [Notes](#notes): Explanation of some of ao3downloader's features and quirks that may not be immediately obvious. I recommend reading this.
- [Known Issues](#known-issues): List of bugs that I know about but haven't yet been able to fix. If you encounter strange behavior, there may be a workaround here.
- [Troubleshooting](#troubleshooting): If you encounter a problem running the script, please read this section carefully and do *all* of the steps in order to the best of your ability before sending a bug report.
- [Contact](#questions-comments-bug-reports): How to get in contact with me. Don't be shy!

## Announcements

Sometimes python version updates break the script, so be careful which version of python you use. See [Troubleshooting](#troubleshooting) if you don't know how to check your python version. The most recent version of python confirmed to work with ao3downloader is: [Python 3.10.8](https://www.python.org/downloads/release/python-3108/)

As of March 8, 2022 I have changed how file names are generated to allow for the inclusion of non-alphanumeric characters (cnovel fans rejoice). If you have a Process going on which relies on file names for the same fic being the same, please take note of this if/when you download the new version of the code.

As of May 14, 2022 I have reduced the maximum length of file and folder names generated by the script from 100 characters to 50 characters. This is to reduce the incidence of download failures caused by exceeding the maximum Windows file path length. Once again, note that this may cause the same fic to be saved under a different name than when it was downloaded previously.

As of September 16, 2022 I have very regretfully removed the series subfolders option, due to the fact that it was causing a huge amount of unnecessary repeated downloads even for people who weren't using it.

As of January 17, 2023 I have changed how file names are generated (again). All file names will now be prefixed with the work id. This is to fix the problem where fics with the same title and author would sometimes overwrite each other in the downloads folder. I have also removed the fandom from the file name, because it was usually gettting cut off by the path length restriction, anyway.

## Instructions

1. install [python](https://www.python.org/downloads/). make sure to install version 3.9.0 or later. see [announcements](#announcements) for the most recent version of python that is confirmed to work with the script - when in doubt, install that version.
2. download the repository as a zip file. the "repository" means the folder containing the code.
    - if you are reading this on [github](https://github.com/nianeyna/ao3downloader), you can download the repository by clicking on the "Code" button in github and selecting "Download ZIP"
    - if you are reading this on [my website](https://nianeyna.dev/ao3downloader/), you can download the repository by clicking the button at the top of the page that says "Click to Download"
3. unzip the zip file you just downloaded. this will create a folder. open it. if you see a file called "ao3downloader.py" then you're in the right place.
4. run the script using the instructions for your operating system:
    - windows: double-click on "ao3downloader.cmd"
    - mac:
        - open a terminal window pointed to the folder containing "ao3downloader.py".
            - You can do this by right-clicking on the folder, going to Services at the bottom of the menu, and clicking "New Terminal at Folder". Alternatively, you can type "cd " and drag the folder to the terminal to copy the folder path.
        - enter the following commands one by one:
        ```txt
        python3 -m venv venv
        source venv/bin/activate
        python3 -m pip install --upgrade pip
        pip install -r requirements.txt
        python3 ao3downloader.py
        ```
        - after this initial setup, when you want to run the program you only need to enter:
        ```txt
        source venv/bin/activate
        python3 ao3downloader.py
        ```
        - note that if you delete the "venv" folder for any reason you will need to do the initial setup again.
    - other platforms: ao3downloader should work on any platform that supports python, however, you will need to do your own research into how to run python programs on your system.

## Menu Options Explanation

- **'<!--CHECK-->download from ao3 link<!--ACTION_DESCRIPTION_AO3-->'** - this works for most links to [ao3](https://archiveofourown.org/). for example, you can use this to download a single work, a series, or any ao3 page that contains links to works or series (such as your bookmarks or an author's works). the program will download multiple pages automatically without the need to enter the next page link manually.
- **'<!--CHECK-->get all work links from an ao3 listing (saves links only)<!--ACTION_DESCRIPTION_LINKS_ONLY-->'** - instead of downloading works, this will simply get a list of all the work links on the page you specify (as well as subsequent pages) and save them in a .txt file inside the downloads folder (one link on each line). this is useful if you prefer to download fics through FanFicFare or some other method, rather than using the ao3 download buttons. this option is much, much faster than a full download - usually only a few seconds per page. when using this option you can also choose to download a csv (spreadsheet) file containing detailed work metadata, instead of a plain text file containing links only.
- **'<!--CHECK-->download links from file<!--ACTION_DESCRIPTION_FILE_INPUT-->'** - allows downloading links from a text file with one work or series link on each line. good if you have already harvested the links you want to download via some other method.
- **'<!--CHECK-->download latest version of incomplete fics<!--ACTION_DESCRIPTION_UPDATE-->'** - you can use this to check a folder on your computer (and any subfolders) for files downloaded from ao3 that are incomplete works. for each incomplete fic found, the program will check ao3 to see if there are any new chapters, and if so, will download the new version to the downloads folder.
- **'<!--CHECK-->download missing fics from series<!--ACTION_DESCRIPTION_UPDATE_SERIES-->'** - checks for files downloaded from ao3 that are part of a series, and for each series found, checks the series page on ao3 and downloads any fics in the series that are not already in your library.
- **'<!--CHECK-->re-download fics saved in one format in a different format<!--ACTION_DESCRIPTION_REDOWNLOAD-->'** - checks for *all* files downloaded from ao3 and redownloads every fic it finds (if possible - failed downloads due to deletion or other reasons will be logged). good if you change your mind about what format you want your library to be in. (file type choices for this option are not saved to settings.)
- **'<!--CHECK-->download marked for later list and mark all as read (requires login)<!--ACTION_DESCRIPTION_MARKED_FOR_LATER-->'** - for those who like to use their marked for later as a download queue, this option takes the headache out of clearing the list after a download. note that this option does not generate 'starting page x' notifications in the console, but will still download all pages.
- **'<!--CHECK-->download bookmarks from pinboard<!--ACTION_DESCRIPTION_PINBOARD-->'** - download ao3 bookmarks from [pinboard](https://pinboard.in/). ignore this if you don't use pinboard. to get the api token go to settings -> password on the pinboard website.
- **'<!--CHECK-->convert logfile into interactable html<!--ACTION_DESCRIPTION_VISUALIZATION-->'** - all downloads from ao3 (and some other actions) are logged in a file called <!--CHECK-->log.jsonl<!--LOG_FILE_NAME--> in the '<!--CHECK-->logs<!--LOG_FOLDER_NAME-->' folder (if this folder does not exist it means no logs have been generated yet), along with information such as whether or not the download was successful, details about errors encountered, and so on. this option converts <!--CHECK-->log.jsonl<!--LOG_FILE_NAME--> into a much more human-readable, searchable and sortable (click on the column headers to sort) html file that can be opened in any browser. the file is called '<!--CHECK-->logvisualization.html<!--VISUALIZATION_FILE_NAME-->' and is saved in the same place as <!--CHECK-->log.jsonl<!--LOG_FILE_NAME-->.
- **'<!--CHECK-->configure ignore list (list of links to never try to download)<!--ACTION_DESCRIPTION_CONFIGURE_IGNORELIST-->'** - creates (if it does not already exist) a file in the main script folder which allows you to specify links to works or series that you never want the script to attempt to download. particularly good if the work or series update option is perpetually grabbing junk you don't want. this option also gives you a chance to auto-add links to the ignore list if they were previously tagged in the log file as failed downloads due to deletion.

## Notes

- **IMPORTANT**: some of your input choices are saved in a file called <!--CHECK-->settings.json<!--SETTINGS_FILE_NAME--> (in the same folder as ao3downloader.py). In some cases you will not be able to change these choices unless you clear your settings by deleting <!--CHECK-->settings.json<!--SETTINGS_FILE_NAME--> (or editing it, if you are comfortable with json). In addition, please note that saved settings include passwords and keys and are saved in plain text. **Use appropriate caution with this file.**
- **The purpose of entering your ao3 login information** is to download archive-locked works or anything else that is not visible when you are not logged in. If you don't care about that, there is no need to enter your login information.
- **Ao3 limits the number of requests** a single user can make to the site in a given time period. When this limit is reached, the script will pause for the amount of time (usually a few minutes) that Ao3 requests. When this happens, the start time, end time, and length of the pause in seconds will be printed to the console. If you try to access Ao3 from your browser during this period, you will see a "Retry later" message. Don't be alarmed by this - it's normal, and you aren't in trouble. Simply wait for the specified amount of time and then refresh the page. Other than during these required pauses, you can use Ao3 as normal while the script is running.
- **If you choose to '<!--CHECK-->get works from series links<!--AO3_PROMPT_SERIES-->'** then if the script encounters a work that is part of a series, it will also download the entire series that the work is a part of. This can *dramatically* extend the amount of time the script takes to run. If you don't want this, choose 'n' when you get this prompt. (Note that this will cause the program to ignore *all* series links, including e.g. series that you have bookmarked.)
- **If you choose to '<!--CHECK-->download embedded images<!--AO3_PROMPT_IMAGES-->'** the script will look for image links on all works it downloads and attempt to save those images to an '<!--CHECK-->images<!--IMAGE_FOLDER_NAME-->' subfolder. Images will be titled with the name of the fic + 'imgxxx' to distinguish them.
    - Note that this feature does not encode any association between the downloaded images and the fic file aside from the file name. 
    - Most file formats will include embedded image files anyway, regardless of whether you choose this option. I have confirmed this for PDF, EPUB, MOBI, and AZW3 file formats. (If you saw me contradict this in an earlier version of this readme... no you didn't)
    - Should an image download fail, the details of the failure will be logged in the log file with the message '<!--CHECK-->Problem getting image<!--ERROR_IMAGE-->' along with the work link and the image link. It's a good idea to check the log file for these messages, since you may still be able to download the image manually or track it down some other way.
- **If you need to stop a download in the middle,** you can just close the window. When you restart the script:
    - If you are using the option '<!--CHECK-->download from ao3 link<!--ACTION_DESCRIPTION_AO3-->', you will be given an option to restart the download from the page you left off on. The program will attempt to avoid re-downloading works that are already in the downloads folder.
    - If you are using the option '<!--CHECK-->download bookmarks from pinboard<!--ACTION_DESCRIPTION_PINBOARD-->' or '<!--CHECK-->re-download fics saved in one format in a different format<!--ACTION_DESCRIPTION_REDOWNLOAD-->', the list of fics to download will be retrieved as normal but will then be filtered to remove work links that meet the following conditions:
        - A record of a download attempt for that link is present in the log file AND
            - There is a fic with the same title already in the downloads folder OR
            - The download was marked as unsuccessful
    - If you are using the option '<!--CHECK-->download latest version of incomplete fics<!--ACTION_DESCRIPTION_UPDATE-->' or '<!--CHECK-->download missing fics from series<!--ACTION_DESCRIPTION_UPDATE_SERIES-->', just make sure to add any fics you don't want to download again to your library (that is, the folder you entered when prompted '<!--CHECK-->input path to folder containing files you want to check for updates<!--UPDATE_PROMPT_INPUT-->') and clean up any old versions before re-starting the download.
    - Most methods of avoiding repeat downloads rely on a file called <!--CHECK-->log.jsonl<!--LOG_FILE_NAME--> which is generated by the script. Make sure not to move, delete, or modify <!--CHECK-->log.jsonl<!--LOG_FILE_NAME--> if you want these features to work. (Using the option to generate the log visualization file is fine.)
- **When checking for incomplete fics,** the code makes certain assumptions about how fic files are formatted. I have tried to make this logic as flexible as possible, but there is still some possibility that not all incomplete fics will be properly identified by the updater, especially if the files are old (since ao3 may have made changes to how they format fics for download over time) or have been edited.
- **Custom work skins** are not preserved in downloaded files. I don't currently have a way around that, however, when a work is downloaded the log entry for the download will contain a column (called 'custom') indicating whether the work had a custom skin or not, so you can at least know which fics are in danger of looking garbled.
- **If you need to keep a different version of python on your system** for some other purpose, please note that these instructions may not work as expected if you have multiple versions of python installed. However, I can point you toward the following resources:
    - Windows: the [py launcher](https://docs.python.org/3/using/windows.html#python-launcher-for-windows) may be helpful to you
    - Mac and Linux: [pyenv](https://github.com/pyenv/pyenv) may be helpful to you

## Known Issues
- With the exception of series links, if you enter a link to an ao3 page that contains links to works or series, but does not support multiple pages of results, the script will loop infinitely. Most notably, this applies to user dashboard pages. If this happens, you can close the window to get out of the loop.
- When downloading missing fics from series, if you are logged in, and the downloader finds a link to a series that is inaccessible because you do not have permission to access the series page, the downloader will download all of the works linked on your user dashboard page, instead. Yes... really.
- Works that contain certain archive messages in either the work text or the tags may cause unexpected behavior. These problem phrases are:
    - <!--CHECK-->Error 404<!--AO3_DELETED-->
    - <!--CHECK-->This work could have adult content.<!--AO3_EXPLICIT-->
    - <!--CHECK-->This work is only available to registered users of the Archive<!--AO3_LOCKED-->

## Troubleshooting
- Make sure you are using python version 3.9.0 or later. To check which version of python you are using:
    - Windows: open a command prompt and enter "python --version"
    - Mac: open a terminal window and enter "python3 --version"
- If you are able to create <!--CHECK-->logvisualization.html<!--VISUALIZATION_FILE_NAME--> (menu option 'v'), take a look through the logs to see if there are any helpful error messages.
- If there are no logs or the logs are unhelpful, look for a folder called "venv" inside the repository. Delete "venv" and try re-running the script.
- If deleting venv doesn't work, try deleting the entire repository and re-downloading from github (but remember to save your existing downloads if you have any!)
- If re-downloading the repository doesn't work, try uninstalling and reinstalling python. 
    - Make sure you install version 3.9.0 or later.
    - Choose "Customize installation" when prompted, and check the "Add Python to environment variables" checkbox when it appears. (This option was previously called "add to PATH"). Everything else can be left as default.
- If reinstalling python doesn't work, [see this stackoverflow answer](https://stackoverflow.com/a/58773979).
- If you have tried all of the above and it still doesn't work, see below for how to send me a bug report.

## Questions? Comments? Bug reports?
Feel free to head over to [the discussion board](https://github.com/nianeyna/ao3downloader/discussions) and make a post, or create an [issue](https://github.com/nianeyna/ao3downloader/issues). I prefer to communicate through the above channels if possible, however I understand many of my users don't have github accounts and may not want to make one just for this, so you can also email me at nianeyna@gmail.com if you prefer. Please include "ao3downloader" in the subject line of emails about the downloader. If you are reporting a bug, please describe exactly what you did to make the bug happen to the best of your ability. (More is more! Be as detailed as possible.)

(Please note that while I will absolutely do my best to get back to you, I can't make any promises - I have a job, etc.)
