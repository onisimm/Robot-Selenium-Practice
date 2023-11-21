from RPA.Browser.Selenium import Selenium
from selenium.common.exceptions import NoSuchElementException

def googleSearch(query, browser = None):
    if browser == None:
        browser = Selenium()
        browser.open_available_browser("https://www.google.com")
        try:
            cookie_popup_close_button = browser.find_element("W0wltc") # W0wltc - Cookie's popup close button name
            if cookie_popup_close_button:
                browser.click_element(cookie_popup_close_button)
        except NoSuchElementException:
            pass

    try:
        search_box = browser.find_element("q") # q - Google textarea's name
        browser.input_text(search_box, query)
        browser.press_keys(search_box, "ENTER")
    except Exception as e:
        print(f"An error occured: {e}")
    
    return browser

def main():
    browser = None
    input_text = input('Enter the text you want to search, or "exit" to exit the program: ')

    while input_text.lower() != "exit":
        browser = googleSearch(input_text, browser)
        input_text = input('Enter the text you want to search, or "exit" to exit the program: ')
    
    print("Cleaning up - closing the browser(s)")
    browser.close_all_browsers()
    
    return

if __name__ == "__main__":
    main()