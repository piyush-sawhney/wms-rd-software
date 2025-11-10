import json
import os

import requests

with open("config/static_config.json", "r") as file:
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


def get_request(doctype, doc_name=None, filters=None, fields=None):
    if doc_name:
        url = f"{base_url}/api/v2/document/{doctype}/{doc_name}"
    else:
        url = f"{base_url}/api/v2/document/{doctype}"
    params = {}
    if filters:
        params["filters"] = json.dumps(filters)
    if fields:
        params["fields"] = json.dumps(fields)

    response = requests.get(url, headers=headers, params=params)

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
        print(f'Creating record for account number {payload['rd_account_number']} with details {payload}.')
        response = requests.post(url, headers=headers, json=payload)
    except requests.RequestException as e:
        print("Request failed:", e)
        return None

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
        print(f'Updating record for account number {doc_name} with details {payload}.')
        response = requests.put(url, headers=headers, json=payload)
    except requests.RequestException as e:
        print("Request failed:", e)
        return None
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
