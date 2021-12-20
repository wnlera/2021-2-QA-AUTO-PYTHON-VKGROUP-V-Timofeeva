import json
from urllib.parse import urljoin

import requests


class ApiMockClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_vk_id(self, username):
        location = "/vk_id/" + username
        url = urljoin(self.base_url, location)

        response = requests.get(url)
        return response

    def create_vk_id(self, username):
        location = "/vk_id/create"
        url = urljoin(self.base_url, location)
        data = {'username': username}
        response = requests.post(url, json=data)
        return response