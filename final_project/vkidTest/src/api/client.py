import json

import requests
from urllib.parse import urljoin
from src.credentials.credentials_api import USERNAME, PASSWORD, EMAIL


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self._authorize()

    def _request(self, method, location, headers=None, files=None, data=None, params=None):
        url = urljoin(self.base_url, location)
        response = self.session.request(method, url, headers=headers, files=files, data=data, params=params)

        return response

    def _authorize(self):
        new_user = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "confirm": PASSWORD,
            "term": "y",
            "submit": "Register"
        }
        location = "/reg"
        res = self._request("POST", location,
                            headers={"Content-Type": "application/x-www-form-urlencoded"},
                            data=new_user)
        if res.status_code == 409:
            user = {
                "username": USERNAME,
                "password": PASSWORD,
                "submit": "Login"
            }
            location = "/login"
            self._request("POST", location,
                          headers={"Content-Type": "application/x-www-form-urlencoded"},
                          data=user)

    def create_user(self, username, password, email):
        location = "/api/add_user"
        data = {"username": username,
                "password": password,
                "email": email}

        response = self._request("POST", location, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        return response

    def delete_user(self, username):
        location = "/api/del_user/" + username
        response = self._request("GET", location)
        return response

    def block_user(self, username):
        location = "/api/block_user/" + username
        response = self._request("GET", location)
        return response

    def accept_user(self, username):
        location = "/api/accept_user/" + username
        response = self._request("GET", location)
        return response

    def get_status(self):
        location = "/status"
        response = self._request("GET", location)
        return response
