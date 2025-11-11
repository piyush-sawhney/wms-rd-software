from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import ids
from config.selenium import driver


def navigate_to_accounts():
    long_waits = WebDriverWait(driver, 30, poll_frequency=5)
    short_waits = WebDriverWait(driver, 10, poll_frequency=1)
    element = short_waits.until(EC.element_to_be_clickable((By.ID, ids.navigation_elements['accounts'])))
    element.click()
    element = long_waits.until(EC.element_to_be_clickable((By.ID, ids.navigation_elements['deposit_accounts'])))
    element.click()
    long_waits.until(EC.element_to_be_clickable((By.ID, ids.navigation_elements['fetch'])))


def navigate_to_aslaas():
    long_waits = WebDriverWait(driver.Instance, 30, poll_frequency=5)
    short_waits = WebDriverWait(driver.Instance, 10, poll_frequency=1)
    element = short_waits.until(EC.element_to_be_clickable((By.ID, ids.navigation_elements['accounts'])))
    element.click()
    element = long_waits.until(EC.element_to_be_clickable((By.ID, ids.navigation_elements['aslaas_update'])))
    element.click()
    long_waits.until(EC.visibility_of_element_located((By.ID, ids.aslaas_update['account_no'])))


def navigate_to_page(page_number):
    short_waits = WebDriverWait(driver.Instance, 30, poll_frequency=5)
    short_waits.until(
        EC.visibility_of_element_located((By.ID, ids.navigation_elements['add_account_page_number'])))
    driver.find_element(By.ID, ids.navigation_elements['add_account_page_number']).send_keys(
        str(page_number))
    driver.find_element(By.ID, ids.navigation_elements['add_account_go']).click()
