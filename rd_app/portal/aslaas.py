from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rd_app.portal import long_waits, short_waits, driver


def update_card_on_portal(rd_account_number, card_number):
    account_element = long_waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.type_AccountId')))
    account_element.clear()
    account_element.send_keys(rd_account_number)
    aslaas_number_element = driver.find_element(By.CSS_SELECTOR, 'input.type_FEBAUnboundString')
    aslaas_number_element.clear()
    aslaas_number_element.send_keys(card_number)
    driver.find_element(By.CSS_SELECTOR, 'input.formbtn_top[value="Continue"]').click()
    add_button = short_waits.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.formbtn_top[value="Add/Update"]')))
    add_button.click()
    success_element = long_waits.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.greenbg')))
    if 'successfully' in success_element.text.lower():
        return True
    else:
        return False
