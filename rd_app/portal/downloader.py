import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from rd_app.portal import short_waits, download_dir, driver
from rd_app.portal.navigation import navigate_to_reports


def parse_date(starting_date):
    if "T" in starting_date:
        starting_date = starting_date.split("T")[0]

    return datetime.strptime(starting_date, "%Y-%m-%d").strftime("%d-%b-%Y")


def search_schedule(schedule_number, starting_date):
    start_date = parse_date(starting_date)
    schedule_number_element = short_waits.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#CustomAgentRDAccountFG\.EBANKING_REF_NUMBER')))
    start_date_element = short_waits.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#CustomAgentRDAccountFG\.REPORT_DATE_FROM')))
    start_date_element.clear()
    start_date_element.send_keys(start_date)
    schedule_number_element.clear()
    schedule_number_element.send_keys(schedule_number)
    element = short_waits.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.formbtn_top')))
    element.click()


def download_schedule_excel():
    dropdown_element = short_waits.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.dropdownexpandalbe_download')))
    dropdown = Select(dropdown_element)
    dropdown.select_by_value("4")
    driver.find_element(By.CSS_SELECTOR, 'input.formbtn_drpdwn').click()


def wait_for_download(timeout=40):
    end_time = time.time() + timeout

    while time.time() < end_time:
        files = os.listdir(download_dir)

        # Chrome temp files on all platforms
        temp_patterns = (
            ".crdownload",  # Windows / normal Chrome
            ".tmp",  # Sometimes temp extension
        )

        # detect in-progress files
        temp_files = [
            f for f in files
            if f.endswith(temp_patterns) or f.startswith(".com.google.Chrome")
        ]

        if temp_files:
            time.sleep(1)
            continue

        # If no temp files → download completed
        if files:
            # Pick the latest created file
            newest_file = max(
                [os.path.join(download_dir, f) for f in files],
                key=os.path.getctime
            )
            return os.path.basename(newest_file), newest_file

        time.sleep(1)

    raise TimeoutError("Download did not complete in time.")


def download_schedule(schedule_details):
    navigate_to_reports()
    search_schedule(schedule_number=schedule_details.get('schedule_number'),
                    starting_date=schedule_details.get('schedule_date'))
    download_schedule_excel()
    return wait_for_download()
