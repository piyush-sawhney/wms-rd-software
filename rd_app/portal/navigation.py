from rd_app.portal import GlobalState, long_waits, driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_accounts():
    long_waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#Accounts'))).click()
    driver.find_element(By.CSS_SELECTOR,"a[name='HREF_Agent Enquire & Update Screen']").click()

def navigate_to_reports():
    long_waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#Accounts'))).click()
    driver.find_element(By.CSS_SELECTOR, "a#Reports").click()