from processor.portal.login_logout import login_to_portal
from processor.portal.navigation import navigate_to_accounts
from processor.portal.schedule_module import fetch_accounts, select_accounts, update_and_verify_account, submit_schedule
from processor.wms.crud import get_request
from processor.wms.wms_processor import update_submitted_schedule, get_draft_schedules


def create_schedules():
    draft_schedules = get_draft_schedules()
    if draft_schedules:
        login_to_portal()
        # update_card_flow()
    for draft_schedule in draft_schedules:
        schedule_details = get_request(doctype="WMS RD Schedule", doc_name=draft_schedule['name'])['data']
        print(schedule_details)
        navigate_to_accounts()
        fetch_accounts(schedule_details)
        select_accounts(schedule_details)
        schedule_details = update_and_verify_account(schedule_details)
        # schedule_number = submit_schedule()

        update_submitted_schedule(schedule_number="12345678", schedule_details=schedule_details)
