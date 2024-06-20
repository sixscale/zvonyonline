import requests

from django.conf import settings

from ..services.logger import log_sz_body
from rest_framework import status

from rest_framework.response import Response


class SkorozvonAPI:
    API_URL = f"https://app.skorozvon.ru/api/v2/"
    _token = None

    # def __init__(self):
    #     self._token = self.get_token()

    # def get_token(self):
    #     token_url = "https://app.skorozvon.ru/oauth/token"
    #     data = {
    #         "grant_type": "password",
    #         "username": settings.SKOROZVON_LOGIN,
    #         "api_key": settings.SKOROZVON_API_KEY,
    #         "client_id": settings.SKOROZVON_APPLICATION_ID,
    #         "client_secret": settings.SKOROZVON_APPLICATION_KEY,
    #     }
    #     response = requests.post(token_url, data=data).json()
    #     return f"Bearer {response['access_token']}"

    def get_request(self, sub_url: str, params: dict = None):
        response = requests.get(
            url=f"{self.API_URL}{sub_url}",
            headers={"Authorization": self._token},
            params=params
        )
        try:
            return response.json()
        except Exception:
            return None

    def get_projects_ids(self):
        response = self.get_request(
            sub_url="call_projects",
            params={"length": 100},
        )
        if not response:
            return None
        return {
            project["title"]: project["id"]
            for project in response["data"]
        }

    def get_scenarios_ids(self):
        response = self.get_request(
            sub_url="scenarios",
            params={"length": 100},
        )
        if not response:
            return None
        return {
            project["name"]: project["id"]
            for project in response["data"]
        }

    def get_users(self):
        users = self.get_request(sub_url="users")
        if not users:
            return None
        return {user["name"]: user["id"] for user in users}

    def get_custom_fields(self):
        params = {
            "length": 100,
        }
        custom_fields = self.get_request(sub_url="custom_fields", params=params)
        if not custom_fields:
            return None
        return custom_fields

    def add_contact(self, contact):
        wr_request_phones = [
            contact.phones_first,
            contact.phones_second,
            contact.phones_third
        ]
        sz_phone_list = [phone for phone in wr_request_phones if phone]
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self._token
        }
        body = {
            "id": str(contact.vid),
            "homepage": contact.site,
            "phones": sz_phone_list,
            "call_project_id": contact.project_id,
            "external_id": str(contact.vid),
            "comment": contact.comment,
            # "custom_fields": {}
        }
        log_sz_body(body)
        response = requests.post(self.API_URL + "liidss", headers=headers, json=body)
        # response = requests.post(self.API_URL + "lead", headers=headers, json=body)
        return response

    def check_if_phone_was_called(self, contact):
        phone = contact.phones_first
        phone_check_data = {
            "phone_to_check": phone,
        }
        url = 'https://usi-col.int3grat.ru/sipuni/index.php'
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, json=phone_check_data, verify=True)
        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")
            return False
        result = response.json()
        return result.get("was_called", False)


skorozvon_api = SkorozvonAPI()
