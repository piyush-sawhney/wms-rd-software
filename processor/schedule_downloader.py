from processor.portal.download_module import search_schedule, download_schedule_excel, wait_for_download
from processor.portal.navigation_module import navigate_to_reports


def schedule_download_flow(schedule_details):
    navigate_to_reports()
    search_schedule(schedule_number=schedule_details['schedule_number'], starting_date=schedule_details['schedule_date'])
    download_schedule_excel()
    return wait_for_download()
