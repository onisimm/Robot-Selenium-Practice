from RPA.Desktop.Windows import Windows
from enum import Enum, unique
from pywinauto.controls import uia_controls
import pyautogui
import time
import os
import pyperclip

@unique
class Option(Enum):
    Exit = 0
    Text = 1
    Photo = 2

def open_app(app_name, window_title) -> Windows:
    win = Windows()
    win.open_from_search(app_name, window_title)
    return win

def get_current_path() -> str:
    folder_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

from html.parser import HTMLParser
import re

class BookmarkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bookmarks = []
        self.current_bookmark = {}

    def handle_data(self, data):
        if self.current_bookmark.get('href'):
            # Extracting only the text part for the name of the bookmark
            name = re.sub(r'\s+', ' ', data.strip())
            if name:
                self.current_bookmark['name'] = name
                self.bookmarks.append(self.current_bookmark)
                self.current_bookmark = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.current_bookmark = {attr[0]: attr[1] for attr in attrs if attr[0] in ['href', 'icon']}

    def handle_data(self, data):
        if self.current_bookmark.get('href'):
            # Extracting only the text part for the name of the bookmark
            name = re.sub(r'\s+', ' ', data.strip())
            if name:
                self.current_bookmark['name'] = name
                self.bookmarks.append(self.current_bookmark)
                self.current_bookmark = {}

def parse_bookmarks(file_path):
    parser = BookmarkParser()
    with open(file_path, 'r', encoding='utf-8') as file:
        parser.feed(file.read())
    return parser.bookmarks

def get_browser_bookmarks():
    win = open_app("chrome", "New Tab - Google Chrome")
    
    pyautogui.hotkey('alt', 'f')
    win.send_keys('b')
    win.send_keys('b')
    time.sleep(0.2)
    win.send_keys('{TAB}')
    win.send_keys('{SPACE}')
    for i in range(4):
        win.send_keys('{DOWN}')
    win.send_keys('{SPACE}')
    time.sleep(0.5)
    bookmarks_path = get_current_path() + "bookmarks.html"
    pyperclip.copy(bookmarks_path)
    win.send_keys('^v')
    try:
        os.remove(bookmarks_path)
    except:
        pass
    win.send_keys('{ENTER}')
    time.sleep(0.2)

    win.close_all_applications()

    return parse_bookmarks(bookmarks_path)

def check_text_in_bookmarks():
    bookmarks = get_browser_bookmarks()

def check_photo_in_bookmarks():
    bookmarks = get_browser_bookmarks()

def output_menu() -> Option:
    print("Choose the option you wish to continue with: ")
    print(" 1: Check if some text is contained in bookmarks and open that bookmark in the browser")
    print(" 2: Check if a photo matches any of the photos of the bookmarks")
    print(" 0: Exit the program")

    while True:
        try:
            user_input = int(input())
            return Option(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid option (0, 1, or 2)")

def main() -> None:
    option = output_menu()

    while option != Option.Exit:
        if (option == Option.Text):
            check_text_in_bookmarks()
        elif (option == Option.Photo):
            check_photo_in_bookmarks()

        option = output_menu()
    
    print("Closing the program.")
    return


if __name__ == "__main__":
    main()