from datetime import datetime

from rd_app.wms.crud import get_request, put_request, post_request, get_request_client, put_request_client, \
    upload_file_to_doc


def get_last_run_details() -> tuple[int, int]:
    response = get_request_client("WMS RD Config")['message']
    return response['last_counter'], response['page_number']


def update_last_run_account_to_wms(i, page_number):
    put_request_client({"doctype": "WMS RD Config","last_counter": int(i), "page_number": int(page_number)})

def update_rd_account(payload):
    payload['last_updated'] = datetime.now().isoformat()
    rd_account_number = payload['rd_account_number']
    put_request(doctype="WMS RD Account", doc_name=rd_account_number, payload=payload)


def create_rd_account(payload):
    payload['last_updated'] = datetime.now().isoformat()
    post_request(doctype="WMS RD Account", payload=payload)

def check_rd_account_exists(rd_account_number):
    return get_request(doctype="WMS RD Account", doc_name=rd_account_number)

def update_account_data(account_data):
    rd_account = check_rd_account_exists(account_data['rd_account_number'])
    if rd_account is not None and len(rd_account) == 0:
        create_rd_account(account_data)
    elif rd_account and len(rd_account) > 0:
        update_rd_account(account_data)

def get_draft_schedules():
    return get_request(doctype="WMS RD Schedule", filters=[["docstatus", "=", 0]])['data']

def get_schedule_details(schedule_name):
    return get_request(doctype="WMS RD Schedule", doc_name=schedule_name)['data']


def upload_schedule(schedule_details, download_path, filename):
    upload_response = upload_file_to_doc(doctype="WMS RD Schedule", doc_name=schedule_details['name'],file_path=download_path, file_name=filename)
    file_url = upload_response["data"]["file_url"]
    put_request(doctype="File", doc_name=upload_response["data"]["name"], payload={"attached_to_field":'schedule_document'})
    put_request(doctype="WMS RD Schedule", doc_name=schedule_details['name'], payload={"docstatus":1, 'schedule_document': file_url})

def update_submitted_schedule(schedule_details):
    schedule_details['schedule_date'] = datetime.today().isoformat()
    return put_request(doctype="WMS RD Schedule", doc_name=schedule_details['name'], payload=schedule_details)