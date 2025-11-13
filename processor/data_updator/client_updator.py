import csv

from processor.data_updator.validators import validate_client_name, validate_client_dob, check_same_number, \
    normalize_date
from processor.wms.crud import get_request, put_request


def get_client_detail_based_on_pan(pan):
    filters = [['pan', '=', pan]]
    client_id = get_request(doctype="WMS Client", filters=filters)['data']
    if len(client_id) > 0:
        return get_request(doctype="WMS Client", doc_name=client_id[0]['name'])['data']
    return None


def get_client_based_on_cif(cif):
    filters = [
        ['WMS Client Codes', 'company_name', 'like', '%post office%'],
        ['WMS Client Codes', 'code', '=', cif]
    ]

    client_list = get_request(doctype="WMS Client", filters=filters)['data']
    if not client_list:
        return None
    client_id = client_list[0]['name']
    return get_request(doctype="WMS Client", doc_name=client_id)['data']


def validate_and_update_details_client(file_row, client_document):
    full_name = " ".join(" ".join([file_row[1], file_row[2], file_row[3]]).split())
    client_document['client_name'] = validate_client_name(full_name, client_document['client_name'])
    if client_document.get('dob') and file_row[26]:
        client_document['dob'] = validate_client_dob(file_row[26], client_document['dob'])
    elif file_row[26]:
        client_document['dob'] = normalize_date(file_row[26])
    if client_document.get('primary_mobile') and file_row[28]:
        if not check_same_number(file_row[28], client_document['primary_mobile']):
            if not file_row[28] in [item['phone'] for item in client_document['numbers'] if 'phone' in item]:
                client_document.setdefault('numbers', []).append({
                    'phone': file_row[28],
                    'is_primary_mobile_no': 0,
                    'is_primary_phone': 0
                })# add a new row to client_document['numbers']
    elif file_row[28]:
        client_document['primary_mobile'] = file_row[28]
    put_request(doctype="WMS Client", doc_name=client_document['name'], payload=client_document)


def process_client_data_from_file(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            file_pan = str(row[0]).strip().upper()
            cif = row[60][1:-1]
            if file_pan and len(file_pan) == 10:
                client_details = get_client_detail_based_on_pan(file_pan)
                if client_details:
                    validate_and_update_details_client(row, client_details)
            elif cif and len(cif) > 3:
                client_details = get_client_based_on_cif(cif)
                if client_details:
                    validate_and_update_details_client(row, client_details)