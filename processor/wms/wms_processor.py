from datetime import datetime

from processor.wms.crud import get_request, post_request, put_request


def update_rd_account(payload):
    payload['last_updated'] = datetime.now().isoformat()
    rd_account_number = payload['rd_account_number']
    payload['rd_account_number'] = None
    put_request(doctype="WMS RD Account", doc_name=rd_account_number, payload=payload)


def create_rd_account(payload):
    payload['last_updated'] = datetime.now().isoformat()
    post_request(doctype="WMS RD Account", payload=payload)


def check_rd_account_exists(rd_account_number):
    return get_request(doctype="WMS RD Account", doc_name=rd_account_number)


def update_rd_account_master(payload):
    rd_account = check_rd_account_exists(payload['rd_account_number'])
    if rd_account is not None and len(rd_account) == 0:
        create_rd_account(payload)
    elif rd_account and len(rd_account) > 0:
        update_rd_account(payload)

def update_submitted_schedule(schedule_number, schedule_details):
    schedule_details['schedule_date'] = datetime.today().isoformat()
    schedule_details['docstatus'] = 1
    schedule_details['schedule_number'] = str(schedule_number).strip()
    put_request(doctype="WMS RD Schedule", doc_name=schedule_details['name'], payload=schedule_details)



def get_draft_schedules():
    return get_request(doctype="WMS RD Schedule", filters=[["docstatus", "=", 0]])['data']