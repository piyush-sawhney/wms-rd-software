from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from rd_app.portal import short_waits, driver


def navigate_to_page(page_number):
    page_number_input = short_waits.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.paginationtxtbx')))
    page_number_input.send_keys(page_number)
    driver.find_element(By.CSS_SELECTOR, 'input.formbtn_pagi_go').click()

def get_end_row_for_page(page_number, total_accounts, total_pages):
    if page_number == total_pages:
        accounts_on_last_page = total_accounts % 10
        if accounts_on_last_page == 0:
            accounts_on_last_page = 10
        return 3 + accounts_on_last_page - 1
    else:
        return 12