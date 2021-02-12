from art import tprint
import requests
import os

import validators


def take_input(placeholder):
    text = input(placeholder)

    if validators.url(text):
        return text
    else:
        return take_input(placeholder)


def make_request(url):
    try:
        r = requests.get(url)

        if r.status_code == 200:

            if "content-disposition" in r.headers:
                filename = get_filename(r.headers.get('content-disposition'))
            elif "Content-Disposition" in r.headers:
                filename = get_filename(r.headers.get('Content-Disposition'))
            else:
                filename = get_filename(url)

            file = {"content": r.content, "filename": filename}

            return file
        else:
            return False

    except:
        print("you fucked up...")
        print("Restarting...")
        os.system('python3 app.py')


def save_to_file(content):
    with open('/Users/ali/Downloads/' + content["filename"], 'wb') as f:
        f.write(content["content"])


def get_filename(text):
    if validators.url(text):
        if text.find('/'):
            return text.rsplit('/', 1)[1]
    else:
        if not text:
            return None
        fname = text.findall('filename=(.+)', text)
        if len(fname) == 0:
            return None
        return fname[0]


if __name__ == '__main__':
    tprint("PyDownloader")
    print("---------------------------------------------------------------------------------")

    input_text = take_input("Paste URL Here: ")

    response = make_request(input_text)

    save_to_file(response)
