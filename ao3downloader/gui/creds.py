from ao3downloader.gui.GuiAction import GuiAction
from ao3downloader import strings
from ao3downloader.gui.shared_gui import Back, Save, can_login
from PySimpleGUI import Button

class CredsGuiAction(GuiAction):
    key = 'c'
    desc = "Enter ao3 credentials"

    def __init__(self, settings: dict):
        super().__init__(settings, "Enter creds")

    def buttons(self):
        self.layout.append([Back(), Save(disabled=True), Button("Clear")])

    def handler(self, event, values, window):
        # only allow saving if we have both a username and a password input
        if event == 'password' or event == 'username':
            state = not can_login(values)
            window['save'].update(disabled=state)

        if event == 'save':            
            self.fileops.save_setting(strings.SETTING_USERNAME, values['username'])
            self.fileops.save_setting(strings.SETTING_PASSWORD, values['password'])
            window['save'].update(disabled=True)
        
        if event == 'Clear':
            window['username'].update('')
            window['password'].update('')
            self.fileops.save_setting(strings.SETTING_USERNAME, '')
            self.fileops.save_setting(strings.SETTING_PASSWORD, '')