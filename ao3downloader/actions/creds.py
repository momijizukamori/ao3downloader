from ao3downloader import strings
from ao3downloader.actions import shared_gui
from ao3downloader.fileio import FileOps

import PySimpleGUI as sg


def gui_action(metadata):
    username = metadata.get('username', '')
    password = metadata.get('password', '')
    layout = [[sg.Text(strings.AO3_PROMPT_USERNAME)],
              [sg.Input(username, key="username", enable_events=True)],
              [sg.Text(strings.AO3_PROMPT_PASSWORD)],
              [sg.Input(password, key="password", password_char="*", enable_events=True)],
              [shared_gui.save(disabled=True), shared_gui.back(), sg.Button("Clear")]
              ]


    def handler(event, values, window):
        fileops = FileOps()

        # only allow saving if we have both a username and a password input
        if event == 'password' or event == 'username':
            state = not shared_gui.can_login(values)
            window['save'].update(disabled=state)

        if event == 'save':            
            fileops.save_setting(strings.SETTING_USERNAME, values['username'])
            fileops.save_setting(strings.SETTING_PASSWORD, values['password'])
            window['save'].update(disabled=True)
        
        if event == 'Clear':
            window['username'].update('')
            window['password'].update('')
            fileops.save_setting(strings.SETTING_USERNAME, '')
            fileops.save_setting(strings.SETTING_PASSWORD, '')

    window = sg.Window("Update credentials", layout, metadata=metadata, finalize=True)
    return window, handler