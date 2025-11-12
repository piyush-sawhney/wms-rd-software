import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
