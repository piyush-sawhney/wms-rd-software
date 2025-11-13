from datetime import datetime

def validate_client_name(file_name, doc_name):
    if file_name.upper() != doc_name:
        return file_name
    return doc_name

def validate_client_dob(file_dob, doc_dob):
    if str(file_dob) != str(doc_dob):
        return normalize_date(file_dob)
    return normalize_date(doc_dob)

def check_same_number(file_mobile, doc_mobile):
    if file_mobile != doc_mobile:
        return False
    return True



def normalize_date(date_str):
    try:
        # input format is DD-MM-YYYY (like 02-02-1962)
        return datetime.strptime(date_str.strip(), "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        # if parsing fails, return as-is (or None)
        return date_str
