from RPA.Desktop.Windows import Windows
from enum import Enum, unique
import pyautogui
import time
import os
import pyperclip
import base64
from PIL import Image
from io import BytesIO
import numpy as np

@unique
class Output_Menu_Option(Enum):
    Exit = 0
    Text = 1
    Photo = 2
    GoBack = 3

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

def get_browser_bookmarks_file() -> bool:
    try:
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
        return True
    except Exception as e:
        print(f"Exception found: {e}")
        return False

def check_text_in_bookmarks(bookmarks):
    inputText = input("Enter the text you want to check: ")

    matchBookmarks = [bookmark for bookmark in bookmarks if inputText.lower() in bookmark['name'].lower()]

    if matchBookmarks != []:
        print("Bookmarks found: ")
        for bookmark in matchBookmarks:
            print(bookmark['name'])

        win = open_app("chrome", "New Tab - Google Chrome")
        first = True
        for bookmark in matchBookmarks:
            if first == False:
                win.send_keys('^t')
            else:
                first = False
            
            pyperclip.copy(bookmark['href'])
            win.send_keys('^l')
            win.send_keys('^v')
            win.send_keys('{ENTER}')
    else:
        print(f"Text '{inputText}' not found in bookmarks\n")

def capture_bookmark_thumbnail(bookmark):
    """ Create an image file from the base64-encoded icon data in the bookmark. """
    icon_data = bookmark['icon'].split(',')[1]
    image_data = base64.b64decode(icon_data)
    image = Image.open(BytesIO(image_data))
    file_name = f"bookmark_{bookmark['name']}.png"
    image.save(file_name)
    return file_name

def images_are_similar(img1_path, img2_path, tolerance=10):
    """
    Compare two images and return True if they are similar within a tolerance.
    Tolerance is the max allowed difference in pixel values (0-255).
    """
    with Image.open(img1_path).convert('RGBA') as img1, Image.open(img2_path).convert('RGBA') as img2:
        if img1.size != img2.size:
            return False

        img1_pixels = np.array(img1)
        img2_pixels = np.array(img2)

        # Calculate the difference
        diff = np.abs(img1_pixels - img2_pixels)
        max_diff = np.max(diff)

        return max_diff <= tolerance

def check_photo_in_bookmarks(bookmarks):
    image_path = input("Enter the path to the image file: ")

    matching_bookmarks = []
    try:
        for bookmark in bookmarks:
            thumbnail_path = capture_bookmark_thumbnail(bookmark)
            if images_are_similar(image_path, thumbnail_path):
                matching_bookmarks.append(bookmark)

        if matching_bookmarks:
            print("Matching bookmarks found:")
            for bookmark in matching_bookmarks:
                print(f"Bookmark: {bookmark['name']}")
            
            win = open_app("chrome", "New Tab - Google Chrome")
            first = True
            for bookmark in matching_bookmarks:
                if not first:
                    win.send_keys('^t')
                else:
                    first = False
                
                pyperclip.copy(bookmark['href'])
                win.send_keys('^l')
                win.send_keys('^v')
                win.send_keys('{ENTER}')
        else:
            print("No matching bookmarks found.")
    finally:
        # Cleanup: Delete the image files created during processing
        for bookmark in bookmarks:
            thumbnail_path = f"bookmark_{bookmark['name']}.png"
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)

def output_menu() -> Output_Menu_Option:
    print("Choose the option you wish to continue with: ")
    print(" 1: Check if some text is contained in bookmarks and open that bookmark in the browser")
    print(" 2: Check if a photo matches any of the photos of the bookmarks")
    print(" 0: Exit the program")

    while True:
        try:
            user_input = int(input())
            return Output_Menu_Option(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid option (0, 1, or 2)")

def bookmarks_menu(bookmarks_path) -> bool:
    if os.path.exists(bookmarks_path):
        print("It seems that you already have the bookmarks file.")
        print("Do you want to reload it? (yes / no)")
        reload = input()

        while reload.lower() != "yes" and reload.lower() != "no":
            print("Invalid input. Please enter 'yes' or 'no'")
            reload = input()

        if (reload.lower() == "yes"):
            return get_browser_bookmarks_file()
        return True
    else:
        print("Creating the bookmarks file. Hold on for a moment")
        time.sleep(1)
        return get_browser_bookmarks_file()

def main() -> None:
    bookmarks_path = get_current_path() + "bookmarks.html"

    if not bookmarks_menu(bookmarks_path):
        print("Something went wrong")
        print("We don't bookmarks to work on.. Failed to create a file")
        return

    print("")

    bookmarks = parse_bookmarks(bookmarks_path)

    option = output_menu()

    while option != Output_Menu_Option.Exit:
        if (option == Output_Menu_Option.Text):
            check_text_in_bookmarks(bookmarks)
        elif (option == Output_Menu_Option.Photo):
            check_photo_in_bookmarks(bookmarks)

        option = output_menu()

    print("Closing the program.")
    return


if __name__ == "__main__":
    main()

    # C:\Projects\Robot-Selenium-Practice\SecondHomework\BookmarksApp\logos\bookmark_Wikipedia.png