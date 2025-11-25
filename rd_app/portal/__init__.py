import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


class GlobalState:
    is_logged_in = False


chrome_options = Options()
download_dir = os.path.join(os.getcwd(), "downloads")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

long_waits = WebDriverWait(driver, 60, poll_frequency=5)
short_waits = WebDriverWait(driver, 15, poll_frequency=1)
