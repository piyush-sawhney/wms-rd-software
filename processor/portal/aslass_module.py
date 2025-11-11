from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import ids, xpaths
from config.selenium import driver


def get_non_updated_card_records():
    pass


def update_card_status_to_wms(account_no):
    pass

def update_card_on_portal(account_no, card_no):
    short_waits = WebDriverWait(driver, 10, poll_frequency=1)
    driver.find_element(By.ID, ids.aslaas_update['account_no']).send_keys(
        account_no.strip())
    driver.find_element(By.ID, ids.aslaas_update['aslaas_number']).send_keys(
        card_no.strip())
    element = short_waits.until(EC.element_to_be_clickable((By.ID, ids.aslaas_update['continue'])))
    element.click()
    element = short_waits.until(EC.element_to_be_clickable((By.ID, ids.aslaas_update['add'])))
    element.click()
    status = short_waits.until(
        EC.presence_of_element_located((By.XPATH, xpaths.schedule_xpath['reference_no']))).text.strip()
    if 'successfully' in status.lower():
        return True
    else:
        return False
