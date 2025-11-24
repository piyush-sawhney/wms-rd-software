import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import ids
from config.selenium import driver



def login_to_portal():
    with open("config/static_config.json", "r") as file:
        config = json.load(file)
    url = config['dop_login_url']
    with open("config/credentials.json", "r") as file:
        config = json.load(file)
    username = config['username']
    password = config['password']
    driver.get(url)
    driver.find_element(By.ID, ids.login_elements['username']).send_keys(username)
    driver.find_element(By.ID, ids.login_elements['password']).send_keys(password)
    long_waits = WebDriverWait(driver, 60, poll_frequency=2)
    long_waits.until(EC.element_to_be_clickable((By.ID, ids.navigation_elements['accounts'])))
