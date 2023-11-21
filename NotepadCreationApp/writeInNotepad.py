from RPA.Desktop.Windows import Windows
import pyperclip
import os, re
import time
import pyautogui
import pygetwindow as gw

def get_folder_path() -> str:
    folder_path = os.path.dirname(os.path.realpath(__file__)) + "\\inputNotepads"
    
    os.makedirs(folder_path, exist_ok=True)

    return folder_path
    

def get_latest_file_number(folder_path) -> int:
    try:
        files = os.listdir(folder_path)
        
        # Get a list with the numbers at the end of "inputNotepad" named notepads existent in the folder
        file_numbers = [int(re.search(r'inputNotepad(\d+)\.txt', file).group(1))
                        for file in files
                        if re.match(r'inputNotepad\d+\.txt', file)]
        
        latest_number = max(file_numbers, default=-1)
    except OSError as e:
        print(f"An error occured: {e}")
    
    return latest_number

def open_app(app_name, window_title) -> Windows:
    win = Windows()
    win.open_from_search(app_name, window_title)

    return win

def get_element_by_name(win, element_name) -> dict:
    elements = win.get_window_elements()

    # The elements variable is a list containing two lists
    # The second list contains dictionaries of element properties
    element_properties = elements[1]

    text_editor_element = None

    text_editor_element = [element for element in element_properties if element['name'] == element_name]

    return text_editor_element


def save_file(win, file_path) -> None:
    win.send_keys('^s')
    time.sleep(1)

    pyperclip.copy(file_path)
    win.send_keys('^v')
    time.sleep(1)

    win.send_keys("{ENTER}")

def activate_window(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]
        if window:
            window.activate()
    except IndexError:
        print(f"No window found with title: {title}")

def main():
    app_name = "notepad.exe"
    window_title = "Untitled - Notepad"
    
    win = open_app(app_name, window_title)
    text_editor_element = get_element_by_name(win, 'Text editor')

    if text_editor_element:
        input_text = input("Enter the text you want to write in the notepad: ")
        # input_text = "testing more words and spaces"
        pyperclip.copy(input_text)

        activate_window(window_title) # Go back to notepad window
        win.send_keys('^v')

        folder_path = get_folder_path()
        filename = "inputNotepad" + str(get_latest_file_number(folder_path) + 1)
        file_path = f"{folder_path}\{filename}.txt"

        save_file(win, file_path)

if __name__ == "__main__":
    main()