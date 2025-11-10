from processor.portal.login_logout import login_to_portal
from processor.portal.navigation import navigate_to_accounts
from processor.wms.crud import get_request


def get_draft_schedules():
    return get_request(doctype="WMS RD Schedule", filters=[["docstatus", "=", 0]])['data']


def create_schedules():
    draft_schedules = get_draft_schedules()
    if draft_schedules:
        login_to_portal()
        navigate_to_accounts()
    for draft_schedule in draft_schedules:
        schedule_details = get_request(doctype="WMS RD Schedule", doc_name=draft_schedule['name'])['data']
        rd_account_numbers = [row["rd_account_number"] for row in schedule_details['rd_accounts']]
