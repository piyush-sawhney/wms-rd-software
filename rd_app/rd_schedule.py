from rd_app.portal import GlobalState
from rd_app.portal.creator import process_schedule
from rd_app.portal.login import login_to_portal
from rd_app.portal.navigation import navigate_to_accounts
from rd_app.wms.processor import get_draft_schedules, get_schedule_details


def process_schedule_creation():
    draft_schedules = get_draft_schedules()
    if draft_schedules:
        if not GlobalState.is_logged_in:
            login_to_portal()
        for draft_schedule in draft_schedules:
            schedule_details = get_schedule_details(draft_schedule['name'])
            print(f"Retrieved Schedule Details {schedule_details}")
            if not schedule_details.get('schedule_number') or not schedule_details.get('schedule_date'):
                navigate_to_accounts()
                process_schedule(schedule_details=schedule_details)
                # fetch_accounts(schedule_details)
                # select_accounts(schedule_details)
                # schedule_number, schedule_date = process_schedule(schedule_details)
                # download_schedule(schedule_number, schedule_date)
                # upload_schedule()
