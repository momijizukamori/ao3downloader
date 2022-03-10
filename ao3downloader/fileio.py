"""File operations go here."""

import datetime
import json
import os
import string

PREFIX = ''

try:
    from google.colab import drive
    PREFIX = '/content/drive'
    drive.mount(PREFIX)

    # Google doesn't have restrictions on length/characters in filenames
    def get_valid_filename(filename):
        return filename

except:
  # we aren't in colab, use local files.

    def get_valid_filename(filename):
        valid_chars = '-_.() {}{}'.format(string.ascii_letters, string.digits)
        valid_name = ''
        for c in filename:
            if c in valid_chars:
                valid_name = valid_name + c
        return valid_name[:100].strip()



def get_setting(filename, setting):
    js = get_json(PREFIX + filename)
    try:
        return js[setting]
    except:
        return ''


def setting(prompt, filename, setting):
    value = get_setting(PREFIX + filename, setting)
    if value == '':
        print(prompt)
        value = input()
        save_setting(PREFIX + filename, setting, value)
    return value


def write_log(filename, log):
    log['timestamp'] = datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    with open(PREFIX + filename, 'a', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False)
        f.write('\n')


def make_dir(folder):
    if not os.path.exists(PREFIX + folder):
        os.mkdir(PREFIX + folder)


def save_bytes(folder, filename, content):
    file = os.path.join(PREFIX, folder, filename)
    with open(file, 'wb') as f:
        f.write(content)



def save_setting(filename, setting, value):
    js = get_json(PREFIX + filename)
    if value is None:
        js.pop(setting, None)
    else:
        js[setting] = value
    with open(PREFIX + filename, 'w') as f:
        f.write(json.dumps(js))


def get_json(filename):
    with open(PREFIX + filename, 'a', encoding='utf-8'):
        pass
    with open(PREFIX + filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return {}

