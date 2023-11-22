from enum import Enum, unique
from RPA.Browser.Selenium import Selenium

def checkTextInBookmarks():
    print("CheckTextInBookmarks")

def checkPhotoInBookmarks():
    print("CheckPhotoInBookmarks")

@unique
class Option(Enum):
    Exit = 0
    Text = 1
    Photo = 2

def outputMenu() -> Option:
    print("Choose the option you wish to continue with: ")
    print(" 1: Check if some text is contained in bookmarks and open that bookmark in the browser")
    print(" 2: Check if a photo matches any of the photos of the bookmarks")
    print(" 0: Exit the program")

    while True:
        try:
            userInput = int(input())
            return Option(userInput)
        except ValueError:
            print("Invalid input. Please enter a valid option (0, 1, or 2)")

def main() -> None:
    option = outputMenu()

    while option != Option.Exit:
        if (option == Option.Text):
            checkTextInBookmarks()
        elif (option == Option.Photo):
            checkPhotoInBookmarks()

        option = outputMenu()
    
    print("Closing the program.")
    return


if __name__ == "__main__":
    main()