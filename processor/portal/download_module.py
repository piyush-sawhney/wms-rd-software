import os
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from config import xpaths, ids
from config.selenium import driver, download_dir
from selenium.webdriver.support import expected_conditions as EC


def parse_date(starting_date):
    if "T" in starting_date:
        starting_date = starting_date.split("T")[0]

    return datetime.strptime(starting_date, "%Y-%m-%d").strftime("%d-%b-%Y")


def search_schedule(schedule_number, starting_date, ending_date=None):
    start_date = parse_date(starting_date)
    short_waits = WebDriverWait(driver, 30, poll_frequency=1)
    short_waits.until(
        EC.element_to_be_clickable((By.ID, ids.schedule_download['schedule_number_input']))
    )
    start_date_element = short_waits.until(
        EC.visibility_of_element_located((By.ID, (ids.reports_download['start_date']))))
    start_date_element.clear()
    start_date_element.send_keys(start_date)
    if ending_date:
        end_date_element = short_waits.until(
            EC.visibility_of_element_located((By.ID, ids.reports_download['end_date'])))
        end_date_element.clear()
        end_date_element.send_keys(start_date)
    schedule_number_element = short_waits.until(
        EC.visibility_of_element_located((By.ID, ids.reports_download['schedule_number'])))
    schedule_number_element.clear()
    schedule_number_element.send_keys(schedule_number)
    element = short_waits.until(EC.element_to_be_clickable((By.ID, ids.reports_download['search_button'])))
    element.click()


def download_schedule_excel():
    short_waits = WebDriverWait(driver, 30, poll_frequency=5)
    element = short_waits.until(EC.element_to_be_clickable((By.XPATH, xpaths.list_download['output_format'])))
    element.click()
    element = short_waits.until(EC.element_to_be_clickable((By.ID, ids.schedule_download['download_file'])))
    driver.execute_script("arguments[0].click();", element)


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