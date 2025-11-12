from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import xpaths, ids
from config.selenium import driver
from processor.portal.login_logout import login_to_portal
from processor.portal.navigation_module import navigate_to_accounts
from processor.wms.wms_processor import update_rd_account_master


def process_accounts():
    long_waits = WebDriverWait(driver, 60, poll_frequency=5)
    start = 0
    counter = 0
    while True:
        rows = driver.find_elements(By.XPATH, xpaths.account_details['table_rows'])
        for i in range(start, (counter + len(rows) - 3)):
            id_of_account = ids.account_details['account_no_summary'] + "[" + str(i) + "]"
            element = long_waits.until(EC.element_to_be_clickable((By.ID, id_of_account)))
            element.click()
            update_account_to_wms()
            driver.find_element(By.ID, ids.navigation_elements['back_button']).click()
            start = start + 1
        counter = start
        next_button = long_waits.until(EC.visibility_of_element_located((By.ID, ids.navigation_elements['page_next'])))
        if next_button.is_enabled():
            next_button.click()
        else:
            break


def update_account_to_wms():
    payload = {
        'rd_account_number': driver.find_element(By.ID, ids.account_details['account_no']).text.strip(),
        'holder_name': driver.find_element(By.ID, ids.account_details['account_name']).text.strip(),
        'account_opening_date': str(
            datetime.strptime(
                driver.find_element(By.ID, ids.account_details['account_opening_date']).text.strip(),
                '%d-%b-%Y').date()),
        'denomination': float(
            driver.find_element(By.ID, ids.account_details['denomination']).text.replace(',', '').strip()),
        'total_deposit_amount': float(
            driver.find_element(By.ID, ids.account_details['total_deposit_amount']).text.replace(',', '').strip()),
        'total_month_paid': int(
            driver.find_element(By.ID, ids.account_details['month_paid_upto']).text.replace(',', '').strip())
    }
    next_installment_date = driver.find_element(By.ID,
                                                ids.account_details['next_installment_date']).text.strip()

    if next_installment_date is not None and next_installment_date != '':
        payload['next_installment_date'] = str(
            datetime.strptime(
                driver.find_element(By.ID, ids.account_details['next_installment_date']).text.strip(),
                '%d-%b-%Y').date())
    else:
        payload['next_installment_date'] = None

    payload['last_deposit_date'] = str(
        datetime.strptime(
            driver.find_element(By.ID, ids.account_details['last_date_of_deposit']).text.strip(),
            '%d-%b-%Y').date())
    payload['rebate'] = float(driver.find_element(By.ID, ids.account_details['rebate']).text.replace(',', '').strip())
    payload['default_fee'] = float(driver.find_element(By.ID, ids.account_details['default_fee']).text.replace(',', '').strip())
    payload['default_installments'] = float(driver.find_element(By.ID, ids.account_details['default_installments']).text.replace(',', '').strip())
    payload['pending_installment'] = float(driver.find_element(By.ID, ids.account_details['pending_installment']).text.replace(',', '').strip())
    update_rd_account_master(payload)



def rd_master_flow():
    login_to_portal()
    navigate_to_accounts()
    process_accounts()
