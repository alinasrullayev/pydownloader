import os

from art import tprint
import requests
import sys
import validators
from requests import RequestException
from tqdm import tqdm
import urllib.parse
import json

if not os.path.exists("settings.json"):
    settings = {"download_path": os.path.expanduser('~/Downloads/')}
    with open('settings.json', 'w') as f:
        json.dump(settings, f)


def main():
    input_text = get_url("Paste URL Here: ")

    try:
        if is_downloadable(input_text):
            r = requests.get(input_text, stream=True)

            save_to_file(r)

        else:
            print("Your url doesn't have valid information to save!")

        if ask_download_again("Do you want to download another file? Y/N: "):
            main()
        else:
            sys.exit(0)

    except RequestException:
        print("you fucked up...")
        print("Restarting...")
        main()


def change_download_path():
    if not os.path.exists("settings.json"):
        settings_dict = {"download_path": get_download_path()}
        with open('settings.json', 'w') as f:
            json.dump(settings_dict, f)
    else:
        with open('settings.json') as f:
            data = json.load(f)

        data['download_path'] = get_download_path()

        with open('settings.json', 'w') as f:
            json.dump(data, f)

    get_menu_choices()


def save_to_file(response):
    with open('settings.json') as f:
        data = json.load(f)

    download_path = data['download_path']

    if "content-disposition" in response.headers:
        filename = get_filename(response.headers.get('content-disposition'))
    elif "Content-Disposition" in response.headers:
        filename = get_filename(response.headers.get('Content-Disposition'))
    else:
        filename = get_filename(response.url)

    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(download_path + filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")


def get_filename(text):
    if validators.url(text):
        decoded_url = urllib.parse.unquote(text)
        if decoded_url.find('/'):
            return decoded_url.rsplit('/', 1)[1]
    else:
        if not text:
            return None
        fname = text.findall('filename=(.+)', text)
        if len(fname) == 0:
            return None
        return fname[0]


def is_downloadable(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def get_menu_choices():
    print("\nMAKE A CHOICE\n")
    print("C - Change Download Path")
    print("D - Download From URL")
    print("Q - Quit")
    print("\n")

    text = input("Your Choice: ").strip()

    if text.lower() == "c":
        change_download_path()
    elif text.lower() == "d":
        main()
    elif text.lower() == "q":
        sys.exit(0)
    else:
        return get_menu_choices()


def get_url(placeholder):
    text = input(placeholder)

    if validators.url(text):
        return text
    else:
        return get_url(placeholder)


def ask_download_again(placeholder):
    text = input(placeholder).strip()

    if text.lower() == "y" or text.lower() == "yes":
        return True
    elif text.lower() == "n" or text.lower() == "no":
        return False
    else:
        return get_url(placeholder)


def get_download_path():
    text = input("Enter New Download Path: ")

    if text.strip() == "":
        return get_download_path()
    else:
        return text


if __name__ == '__main__':
    tprint("PyDownloader")
    print("---------------------------------------------------------------------------------\n")


    try:
        get_menu_choices()
    except KeyboardInterrupt:
        sys.exit(0)
