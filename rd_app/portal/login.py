import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rd_app.portal import GlobalState, driver, long_waits


def login_to_portal():
    with open("rd_app/config/static_config.json", "r") as file:
        config = json.load(file)
    url = config['login_url']
    with open("rd_app/config/credentials.json", "r") as file:
        config = json.load(file)
    username = config['username']
    password = config['password']
    driver.get(url)
    long_waits.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input#VALIDATE_RM_PLUS_CREDENTIALS_CATCHA_DISABLED')))
    driver.find_element(By.CSS_SELECTOR, 'input.txtfield').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, 'input.txtField').send_keys(password)
    long_waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#Accounts')))
    GlobalState.is_logged_in = True
