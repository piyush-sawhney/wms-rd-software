from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import xpaths, ids
from config.selenium import driver
from processor.portal.navigation import navigate_to_page


def fetch_accounts(schedule_details):
    rd_schedule_type = 'cash' if schedule_details['schedule_type'].lower() == "cash" else 'cheque'
    account_nos = ','.join([item['rd_account_number'] for item in schedule_details['rd_accounts']])
    driver.find_element(By.XPATH, xpaths.schedule_xpath[rd_schedule_type]).click()
    account_no_search_element = driver.find_element(By.ID, ids.schedule_elements['search'])
    account_no_search_element.clear()
    account_no_search_element.send_keys(account_nos)
    driver.find_element(By.ID, ids.navigation_elements['fetch']).click()


def select_accounts(schedule_details):
    number_of_accounts = len(schedule_details['rd_accounts'])
    for i in range(1, number_of_accounts + 1):
        element_id = ids.schedule_elements['account_no_check_box'] + f"[{i - 1}]"
        short_waits = WebDriverWait(driver, 45, poll_frequency=2)
        short_waits.until(EC.visibility_of_element_located((By.ID, element_id)))
        driver.find_element(By.ID, element_id).click()
        if not i == 0 and i % 10 == 0 and number_of_accounts != 10:
            driver.find_element(By.ID, ids.navigation_elements['next_select_account']).click()
    driver.find_element(By.ID, ids.schedule_elements['save_accounts']).click()


def verify_account(i, number_of_accounts):
    short_waits = WebDriverWait(driver, 30, poll_frequency=5)
    page_to_go = int(((i + 1) / 10) + 1)

    element_id_string = ids.schedule_elements['modified_status'] + f"[{i}]"
    if i <= 9:
        assert short_waits.until(
            EC.visibility_of_element_located((By.ID, element_id_string))).text.strip().lower() == 'yes'
        if i == 9 and number_of_accounts != 10:
            navigate_to_page(page_to_go)
    elif i % 10 == 9:
        navigate_to_page(page_to_go - 1)
        assert short_waits.until(
            EC.visibility_of_element_located((By.ID, element_id_string))).text.strip().lower() == 'yes'
        navigate_to_page(page_to_go)
    else:
        navigate_to_page(page_to_go)
        assert short_waits.until(
            EC.visibility_of_element_located((By.ID, element_id_string))).text.strip().lower() == 'yes'


def update_and_verify_account(schedule_details):
    rd_accounts = sorted(schedule_details['rd_accounts'], key=lambda x: x['rd_account_number'])
    for i in range(len(schedule_details['rd_accounts'])):
        short_waits = WebDriverWait(driver, 45, poll_frequency=2)
        element_id_string = ids.schedule_update_elements['account_no'] + f"[{i}]"
        account_no = short_waits.until(EC.visibility_of_element_located((By.ID, element_id_string))).text.strip()
        assert account_no == rd_accounts[i]['rd_account_number']
        radio_button_xpath = xpaths.account_details['radio_button'].replace("{value}", str(i))
        driver.find_element(By.XPATH, radio_button_xpath).click()
        # Rebate and Default Calculation
        no_of_installment_element = driver.find_element(By.ID, ids.schedule_elements['no_of_installment'])
        no_of_installment_element.clear()
        no_of_installment_element.send_keys(rd_accounts[i]['number_of_installments'])
        driver.find_element(By.ID, ids.schedule_elements['rebate_default_button']).click()
        rebate_element = short_waits.until(
            EC.presence_of_element_located((By.ID, ids.schedule_elements['rebate'])))
        default_element = short_waits.until(
            EC.presence_of_element_located((By.ID, ids.schedule_elements['default'])))
        rd_accounts[i]['rebate'] = float(rebate_element.text.replace(",", "").strip())
        rd_accounts[i]['surcharge'] = float(default_element.text.replace(",", "").strip())

        # Update cheque details
        if schedule_details['schedule_type'] == "cheque":
            cheque_no_element = driver.find_element(By.ID, ids.schedule_elements['cheque_no'])
            cheque_no_element.clear()
            cheque_no_element.send_keys(rd_accounts[i]['cheque_number'])
            cheque_acc_no_element = driver.find_element(By.ID, ids.schedule_elements['cheque_acc_no'])
            cheque_acc_no_element.clear()
            cheque_acc_no_element.send_keys(rd_accounts[i]['bank_account_number'])

        driver.find_element(By.ID, ids.schedule_elements['save_modification']).click()
        verify_account(i, len(schedule_details['rd_accounts']))
    schedule_details['rd_accounts'] = rd_accounts
    return schedule_details


def submit_schedule():
    short_waits = WebDriverWait(driver, 15, poll_frequency=2)
    driver.find_element(By.ID, ids.schedule_elements['pay_schedule']).click()
    ref_no_text = short_waits.until(
        EC.visibility_of_element_located((By.XPATH, xpaths.schedule_xpath['reference_no']))).text.strip()
    print(ref_no_text)
    reference_no = ref_no_text.split(".")[1]
    reference_no = reference_no[reference_no.rindex(" "):].strip()
    print(reference_no)
    return reference_no
