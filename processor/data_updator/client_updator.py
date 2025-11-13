import csv

from processor.wms.crud import get_request


def get_client_detail_based_on_pan(pan):
    filters = [['pan', '=', pan]]
    return get_request(doctype="WMS Client", filters=filters)


def get_client_based_on_cif(cif):
    filters = [['company_name', 'like', 'post office'], ['code', '=', cif]]
    fields = ['parent']
    client_name = get_request(doctype="WMS Client Codes", filters=filters, fields=fields)
    return get_request(doctype="WMS Client", doc_name=client_name)


def validate_and_update_client_details(file_row, client_document):
    pass


def process_client_data_from_file(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
    for row in reader:
        file_pan = str(row[0]).strip().upper()
        client_details = get_client_detail_based_on_pan(file_pan)
        if client_details:
            validate_and_update_client_details(row, client_details)
        else:
            cif = row[59][1:-1]
            client_details = get_client_based_on_cif(cif)
            if client_details:
                validate_and_update_client_details(row, client_details)
