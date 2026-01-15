import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rd_app.portal import driver, short_waits, long_waits
from rd_app.portal.common import navigate_to_page


def fetch_accounts(schedule_details):
    long_waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='C']")))
    driver.find_element(By.CSS_SELECTOR, "input[value='C']").click() if schedule_details[
                                                                            'schedule_type'].lower() == "cash" else driver.find_element(
        By.CSS_SELECTOR, "input[value='DC']").click()
    account_nos = ','.join([item['rd_account_number'] for item in schedule_details['rd_accounts']])
    account_no_search_element = driver.find_element(By.CSS_SELECTOR, 'textarea')
    account_no_search_element.clear()
    account_no_search_element.send_keys(account_nos)
    driver.find_element(By.CSS_SELECTOR, 'input#Button3087042').click()


def select_accounts(schedule_details):
    number_of_accounts = len(schedule_details['rd_accounts'])
    for i in range(0, number_of_accounts):
        element_id = f'CustomAgentRDAccountFG.SELECT_INDEX_ARRAY[{i}]'
        checkbox_element = short_waits.until(EC.element_to_be_clickable((By.ID, element_id)))
        checkbox_element.click()
        if (i != number_of_accounts - 1) and ((i + 1) % 10 == 0):
            page_number = (i // 10) + 1
            navigate_to_page(page_number + 1)
    driver.find_element(By.CSS_SELECTOR, 'input#Button26553257').click()


def save_account(i, row, account_number, number_of_installments, schedule_type=None, cheque_number=None,
                 bank_account_number=None) -> tuple[float, float]:
    radio_button = short_waits.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"input.absmiddle[value='{i}']")))
    account_no_element = driver.find_element(By.CSS_SELECTOR, f'tr:nth-of-type({row + 2}) td:nth-of-type(2) span')
    assert account_number == account_no_element.text.strip()
    radio_button.click()
    installment_element = driver.find_element(By.CSS_SELECTOR, "input[name='CustomAgentRDAccountFG.RD_INSTALLMENT_NO']")
    installment_element.clear()
    installment_element.send_keys(number_of_installments)
    rebate_default_button = short_waits.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"input#Button22426525")))
    rebate_default_button.click()
    time.sleep(1)
    rebate_element = short_waits.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'p:nth-of-type(3) span.simpletext')))
    default_element = driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(4) span.simpletext')
    rebate = float(rebate_element.text.replace(",", "").strip())
    default = float(default_element.text.replace(",", "").strip())

    if schedule_type == "cheque":
        cheque_no_element = driver.find_element(By.CSS_SELECTOR, 'input.type_FEBAUnboundString')
        cheque_no_element.clear()
        cheque_no_element.send_keys(cheque_number)
        cheque_acc_no_element = driver.find_element(By.CSS_SELECTOR, 'input.type_AccountId')
        cheque_acc_no_element.clear()
        cheque_acc_no_element.send_keys(bank_account_number)

    save_button = driver.find_element(By.CSS_SELECTOR, 'input#Button11874602')
    save_button.click()
    return rebate, default


def verify_account(i, row, account_number, schedule_type):
    modified_row_number = 10 if schedule_type.lower() == "cash" else 12
    short_waits.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f"input.absmiddle[value='{i}']")))
    account_no_element = driver.find_element(By.CSS_SELECTOR, f'tr:nth-of-type({row + 2}) td:nth-of-type(2) span')
    assert account_number == account_no_element.text.strip()
    modified_element = driver.find_element(By.CSS_SELECTOR, f'tr:nth-of-type({row + 2}) td:nth-of-type({modified_row_number}) span')
    assert modified_element.text.strip().lower() == "yes"


def submit_schedule():
    driver.find_element(By.CSS_SELECTOR, 'input#PAY_ALL_SAVED_INSTALLMENTS').click()
    time.sleep(1)
    ref_no_text = short_waits.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.greenbg'))).text.strip()
    print(ref_no_text)
    reference_no = ref_no_text.split(".")[1]
    reference_no = reference_no[reference_no.rindex(" "):].strip()
    print(reference_no)
    return reference_no

def process_schedule(schedule_details):
    rd_accounts = sorted(schedule_details['rd_accounts'], key=lambda x: x['rd_account_number'])
    fetch_accounts(schedule_details)
    select_accounts(schedule_details)
    for i in range(len(rd_accounts)):
        page_of_i = (i // 10) + 1
        row_of_i = (i % 10) + 1
        if page_of_i != 1:
            navigate_to_page(page_of_i)
        if schedule_details['schedule_type'].lower() == "cash":
            rebate, default = save_account(i=i, row=row_of_i, account_number=rd_accounts[i]['rd_account_number'],
                                           number_of_installments=rd_accounts[i]['number_of_installments'])
        else:
            rebate, default = save_account(i=i, row=row_of_i, account_number=rd_accounts[i]['rd_account_number'],
                                           number_of_installments=rd_accounts[i]['number_of_installments'],
                                           schedule_type="cheque", cheque_number=rd_accounts[i]['cheque_number'],
                                           bank_account_number=rd_accounts[i]['bank_account_number'])
        rd_accounts[i]['rebate'] = rebate
        rd_accounts[i]['surcharge'] = default
        if page_of_i != 1:
            navigate_to_page(page_of_i)
        verify_account(i=i, row=row_of_i, account_number=rd_accounts[i]['rd_account_number'],schedule_type=schedule_details['schedule_type'])
    schedule_details['rd_accounts'] = rd_accounts
    schedule_number = submit_schedule()
    schedule_details['schedule_number'] = str(schedule_number).strip()
    return schedule_details
