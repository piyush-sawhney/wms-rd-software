from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import xpaths, ids
from config.selenium import driver


def fetch_accounts(account_list, is_cash):
    schedule_type = 'cash' if is_cash else 'cheque'
    account_nos = ','.join([item[0] for item in account_list])
    driver.find_element(By.XPATH, xpaths.schedule_xpath[schedule_type]).click()
    account_no_search_element = driver.find_element(By.ID, ids.schedule_elements['search'])
    account_no_search_element.clear()
    account_no_search_element.send_keys(account_nos)
    driver.find_element(By.ID, ids.navigation_elements['fetch']).click()


def select_accounts(account_list):
    number_of_accounts = len(account_list)
    for i in range(1, number_of_accounts + 1):
        element_id = ids.schedule_elements['account_no_check_box'] + f"[{i - 1}]"
        short_waits = WebDriverWait(driver, 45, poll_frequency=2)
        short_waits.until(EC.visibility_of_element_located((By.ID, element_id)))
        driver.find_element_by_id(element_id).click()
        if not i == 0 and i % 10 == 0 and number_of_accounts != 10:
            driver.find_element(By.ID, ids.navigation_elements['next_select_account']).click()
    driver.find_element(By.ID, ids.schedule_elements['save_accounts']).click()
