import re
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rd_app.portal import long_waits, short_waits, driver
from rd_app.wms.processor import update_account_data, update_last_run_account_to_wms


def navigate_to_counter_account_page(counter) -> int:
    page_number = (counter // 10) + 1
    navigate_to_page(page_number)
    return page_number


def get_total_accounts_and_page_numbers() -> tuple[int, int]:
    total_account_element = long_waits.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.right span.tablesimpletext')))
    total_accounts = int(re.search(r'of\s+(\d+)', total_account_element.text).group(1))
    total_pages = (total_accounts + 10 - 1) // 10
    return total_accounts, total_pages


def navigate_to_page(page_number):
    page_number_input = short_waits.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.paginationtxtbx')))
    page_number_input.send_keys(page_number)
    driver.find_element(By.CSS_SELECTOR, 'input.formbtn_pagi_go').click()


def extract_account_data(account_number) -> dict:
    account_no_element = short_waits.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'p:nth-of-type(1) span.searchsimpletext')))
    if account_number != account_no_element.text.strip():
        raise
    account_data = {
        'rd_account_number': account_no_element.text.strip(),
        'holder_name': driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(2) span.searchsimpletext').text.strip(),
        'account_opening_date': str(
            datetime.strptime(
                driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(3) span.searchsimpletext').text.strip(),
                '%d-%b-%Y').date()),
        'denomination': float(
            driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(4) span.simpletext').text.replace(',',
                                                                                                  '').strip()),
        'total_deposit_amount': float(
            driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(5) span.simpletext').text.replace(',',
                                                                                                  '').strip()),
        'total_month_paid': int(
            driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(6) span.searchsimpletext').text.replace(',',
                                                                                                        '').strip()),
        'last_deposit_date': str(
            datetime.strptime(
                driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(8) span.searchsimpletext').text.strip(),
                '%d-%b-%Y').date()),
        'rebate': float(driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(9) span.searchsimpletext').text.replace(',',
                                                                                                                    '').strip()),
        'default_fee': float(
            driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(10) span.searchsimpletext').text.replace(',',
                                                                                                         '').strip()),
        'default_installments': float(
            driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(11) span.searchsimpletext').text.replace(',',
                                                                                                         '').strip()),
        'pending_installment': float(
            driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(12) span.searchsimpletext').text.replace(',',
                                                                                                         '').strip()),

    }
    next_installment_date = driver.find_element(By.CSS_SELECTOR, 'p:nth-of-type(7) span.searchsimpletext').text.strip()
    if next_installment_date is not None and next_installment_date != '':
        account_data['next_installment_date'] = str(
            datetime.strptime(next_installment_date, '%d-%b-%Y').date())
    else:
        account_data['next_installment_date'] = None
    return account_data


def process_account(i):
    dynamic_selector = f'tr:nth-of-type({i}) a'
    account_element = long_waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, dynamic_selector)))
    account_number = account_element.text
    account_element.click()
    account_data = extract_account_data(account_number)
    update_account_data(account_data)
    driver.find_element(By.CSS_SELECTOR, 'input.formbtn_last').click()


def process_accounts_on_a_page(start_row, end_row, page_number):
    for i in range(start_row, end_row + 1):
        try:
            process_account(i)
        except Exception as e:
            update_last_run_account_to_wms(i, page_number)
            raise e


def get_end_row_for_page(page_number, total_accounts, total_pages):
    if page_number == total_pages:
        accounts_on_last_page = total_accounts % 10
        if accounts_on_last_page == 0:
            accounts_on_last_page = 10
        return 3 + accounts_on_last_page - 1
    else:
        return 12


def process_rd_accounts(row, page_number):
    total_account_count, page_number_count = get_total_accounts_and_page_numbers()
    for page_number in range(page_number, page_number_count):
        start_row = 3 + (row % 10)
        end_row = get_end_row_for_page(page_number, total_account_count, page_number_count)
        process_accounts_on_a_page(start_row, end_row, page_number)
        navigate_to_page(page_number + 1)
