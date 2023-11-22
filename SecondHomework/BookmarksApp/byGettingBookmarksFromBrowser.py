# TO FINISH THE IMAGE PART

from RPA.Desktop.Windows import Windows
from enum import Enum, unique
from pywinauto.controls import uia_controls
import pyautogui
import pyperclip
import time

@unique
class Option(Enum):
    Exit = 0
    Text = 1
    Photo = 2

def open_app(app_name, window_title) -> Windows:
    chromeWindow = Windows()
    chromeWindow.open_from_search(app_name, window_title)
    return chromeWindow

def get_window_element_bookmarks(chromeWindow) -> list:
    elements = chromeWindow.get_window_elements()

    # The elements variable is a list containing two lists
    # The second list contains dictionaries of element properties
    element_properties = elements[1]

    # Now, find all button elements that are children of this toolbar
    bookmarks = [element for element in element_properties
                 if 'object' in element 
                 and isinstance(element['object'], uia_controls.ButtonWrapper) 
                 and element['parent'] == 'ToolBar' 
                 and element['name'] != '']  # Assuming bookmark buttons have non-empty names
    
    bookmarks_dict = {}

    for bookmark in bookmarks:
        name = bookmark.get('name')
        href = bookmark['legacy'].get('Description')  # Assuming URL is in the 'Description' field
        if name and href:
            bookmarks_dict[name] = href

    return bookmarks_dict


def get_browser_bookmarks():
    chromeWindow = open_app("chrome", "Google Chrome")
    bookmarks = get_window_element_bookmarks(chromeWindow)

    return [chromeWindow, bookmarks]

def check_text_in_bookmarks(chromeWindow, bookmarks, first):

    print("let's seeee")
    input_text = input("Enter the text you want to check: ")

    matchBookmarks = {key: value for key, value in bookmarks.items() if input_text.lower() in key.lower()}

    if matchBookmarks != []:
        print("Bookmarks found: ")
        print(matchBookmarks.keys())
        
        time.sleep(2)
        pyautogui.hotkey('alt', 'tab')

        for name in matchBookmarks:
            if first == False:
                chromeWindow.send_keys('^t')
            else:
                first = False
            
            pyperclip.copy(matchBookmarks[name])
            chromeWindow.send_keys('^l')
            chromeWindow.send_keys('^v')
            chromeWindow.send_keys('{ENTER}')
    else:
        print(f"Text '{input_text}' not found in bookmarks\n")

def check_photo_in_bookmarks(chromeWindow, bookmarks, first):
    pyautogui.hotkey('alt', 'tab')

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
    print("\n\nGetting the bookmarks..")
    chromeWindow, bookmarks = get_browser_bookmarks()
    print(" -> Got the bookmarks\n")

    pyautogui.hotkey('alt', 'space')
    pyautogui.press('n')

    option = output_menu()

    first = True
    while option != Option.Exit:
        if (option == Option.Text):
            check_text_in_bookmarks(chromeWindow, bookmarks, first)
        elif (option == Option.Photo):
            check_photo_in_bookmarks(chromeWindow, bookmarks, first)

        option = output_menu()

    print("Closing the program.")
    return

if __name__ == "__main__":
    main()