import json
import os

import requests

with open("rd_app/config/static_config.json", "r") as file:
    config = json.load(file)
base_url = config['base_url']
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

if not api_key or not api_secret:
    raise ValueError("Missing API_KEY or API_SECRET in environment variables")
headers = {
    "Authorization": f"token {api_key}:{api_secret}",
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_request_client(doctype):
    url = f"{base_url}/api/method/frappe.client.get"
    params = {}

    if doctype:
        params['doctype'] = doctype
    try:
        print(f'Getting {doctype} through frappe get client.')
        response = requests.get(url, headers=headers, params=params)
    except requests.RequestException as e:
        raise requests.HTTPError(
            f"Request failed {e}"
        )
    if response.status_code == 200:
        return response.json()
    else:
        try:
            error_data = response.json()
        except json.JSONDecodeError:
            error_data = {"error": response.text}
        raise requests.HTTPError(
            f"Request failed with status {response.status_code}: {error_data}"
        )

def put_request_client(payload):
    url = f"{base_url}/api/method/frappe.client.save"
    doc_str = json.dumps(payload)
    data = {
        "doc": doc_str
    }
    upload_headers = {
        "Authorization": headers["Authorization"],
        "Accept": "application/json"
    }
    try:
        print(f'Updating {payload} through frappe client.')
        response = requests.put(url, headers=upload_headers, data=data)
    except requests.RequestException as e:
        print("Request failed:", e)
        raise

    if response.status_code == 200:
        return response.json()
    else:
        try:
            error_data = response.json()
        except json.JSONDecodeError:
            error_data = {"error": response.text}
        raise requests.HTTPError(
            f"Request failed with status {response.status_code}: {error_data}"
        )
def get_request(doctype, doc_name=None, filters=None, fields=None, or_filters=None):
    if doc_name:
        url = f"{base_url}/api/v2/document/{doctype}/{doc_name}"
    else:
        url = f"{base_url}/api/v2/document/{doctype}"
    params = {}
    if filters:
        params["filters"] = json.dumps(filters)
    if fields:
        params["fields"] = json.dumps(fields)
    if or_filters:
        params["or_filters"] = json.dumps(or_filters)
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.RequestException as e:
        raise requests.HTTPError(
            f"Request failed {e}"
        )
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        try:
            data = response.json()
            if data.get('errors') and data['errors'][0].get('type') == "DoesNotExistError":
                print(f"Document {doc_name} does not exist.")
                return {}
        except json.JSONDecodeError:
            print("Response is not valid JSON:", response.text)
            raise
    else:
        try:
            error_data = response.json()
        except json.JSONDecodeError:
            error_data = {"error": response.text}
        raise requests.HTTPError(
            f"Request failed with status {response.status_code}: {error_data}"
        )


def post_request(doctype, payload):
    url = f"{base_url}/api/v2/document/{doctype}"
    try:
        print(f'Creating record for {doctype} with details {payload}.')
        response = requests.post(url, headers=headers, json=payload)
    except requests.RequestException as e:
        print("Request failed:", e)
        raise

    if response.status_code == 200:
        return response.json()
    else:
        try:
            error_data = response.json()
        except json.JSONDecodeError:
            error_data = {"error": response.text}
        raise requests.HTTPError(
            f"Request failed with status {response.status_code}: {error_data}"
        )


def put_request(doctype, doc_name, payload):
    url = f"{base_url}/api/v2/document/{doctype}/{doc_name}"
    try:
        print(f'Updating record for {doctype}: {doc_name} with details {payload}.')
        response = requests.put(url, headers=headers, json=payload)
    except requests.RequestException as e:
        print("Request failed:", e)
        raise
    if response.status_code == 200:
        return response.json()['data']
    else:
        try:
            error_data = response.json()
        except json.JSONDecodeError:
            error_data = {"error": response.text}
        raise requests.HTTPError(
            f"Request failed with status {response.status_code}: {error_data}"
        )

def upload_file_to_doc(file_name, file_path, doctype, doc_name, is_private=1):
    url = f"{base_url}/api/v2/method/upload_file"

    upload_headers = {
        "Authorization": headers["Authorization"],
        "Accept": "application/json"
    }

    try:
        with open(file_path, "rb") as file:
            files = {"file": (file_name, file)}
            data = {
                "doctype": doctype,
                "docname": doc_name,
                "is_private": is_private,
                "folder": "Home/RD Schedules",
            }
            print(f"Uploading file {file_path} to DocType: {doctype} with Doc Name {doc_name}.")
            response = requests.post(
                url, headers=upload_headers, files=files, data=data
            )

        # Raise exception for non-200 codes
        response.raise_for_status()
        return response.json()

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except requests.HTTPError as e:
        # Try parse JSON error
        try:
            server_error = response.json()
        except:
            server_error = response.text

        raise Exception(f"Upload failed ({response.status_code}): {server_error}") from e

    except Exception as e:
        raise Exception(f"Unexpected error uploading file: {str(e)}")