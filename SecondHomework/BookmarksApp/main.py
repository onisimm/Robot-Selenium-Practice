from RPA.Desktop.Windows import Windows
from enum import Enum, unique
from pywinauto.controls import uia_controls

@unique
class Option(Enum):
    Exit = 0
    Text = 1
    Photo = 2

def open_app(app_name, window_title) -> Windows:
    win = Windows()
    win.open_from_search(app_name, window_title)
    return win

def get_window_element_bookmarks(win) -> list:
    elements = win.get_window_elements()

    # The elements variable is a list containing two lists
    # The second list contains dictionaries of element properties
    element_properties = elements[1]

    # Now, find all button elements that are children of this toolbar
    bookmarks = [element for element in element_properties
                 if 'object' in element 
                 and isinstance(element['object'], uia_controls.ButtonWrapper) 
                 and element['parent'] == 'ToolBar' 
                 and element['name'] != '']  # Assuming bookmark buttons have non-empty names

    return bookmarks

def get_browser_bookmarks():
    win = open_app("chrome", "New Tab - Google Chrome")
    bookmarks_element = get_window_element_bookmarks(win)

    print(bookmarks_element)

def check_text_in_bookmarks():
    get_browser_bookmarks()

def check_photo_in_bookmarks():
    get_browser_bookmarks()

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