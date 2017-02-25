from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Firefox()
browser.get("http://www.google.com")
print 'page title before search: {0}'.format(browser.title)

inputElement = browser.find_element_by_name("q")
inputElement.send_keys("seleniumhq")
inputElement.submit()

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(browser, 10).until(expected_conditions.title_contains("seleniumhq"))
    print 'search results title: {0}'.format(browser.title)

finally:
    browser.quit()