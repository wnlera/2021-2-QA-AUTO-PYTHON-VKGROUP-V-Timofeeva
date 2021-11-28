import logging
from urllib.parse import urljoin
import json

import requests

from sources.const_campaign import campaign, segment

logger = logging.getLogger('test')
MAX_RESPONSE_LENGTH = 666


class InvalidLoginException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class ApiClient:
    def __init__(self, base_url, user, password):
        self.base_url = base_url
        self.user = user
        self.password = password

        self.session = requests.Session()
        self.csrf_token = None
        try:
            self._authorize()
        except Exception as e:
            raise InvalidLoginException(e)

    @property
    def headers(self):
        return {
            "X-CSRFToken": self.csrf_token
        }

    @property
    def auth_headers(self):
        return {
            "Referer": self.base_url
        }

    @staticmethod
    def log_before_request(url, headers, data, expected_status):
        logger.info(f'Performing request:\n'
                    f'URL: {url}\n'
                    f'HEADERS: {headers}\n'
                    f'DATA: {data}\n'
                    f'expected status: {expected_status}\n')

    @staticmethod
    def log_after_request(response):
        log_str = f'Got response:\n' \
                  f'RESPONSE STATUS: {response.status_code}'

        if len(response.text) > MAX_RESPONSE_LENGTH:
            if logger.level == logging.INFO:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: COLLAPSED due to response size > {MAX_RESPONSE_LENGTH}. '
                            f'Use DEBUG logging.\n\n'
                            f'{response.text[:MAX_RESPONSE_LENGTH]}')
            elif logger.level == logging.DEBUG:
                logger.info(f'{log_str}\n'
                            f'RESPONSE CONTENT: {response.text}\n')
        else:
            logger.info(f'{log_str}\n'
                        f'RESPONSE CONTENT: {response.text}\n')

    def _request(self, method, location, headers=None, files=None, data=None, params=None, expected_status=200,
                 jsonify=True):
        url = urljoin(self.base_url, location)
        self.log_before_request(url, headers, data, expected_status)
        headers = headers or self.headers
        response = self.session.request(method, url, headers=headers, files=files, data=data, params=params)
        self.log_after_request(response)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.request} for URL "{url}"')

        if jsonify:
            return response.json()
        return response

    def get_segment(self, id_=None):
        location = "/api/v2/coverage/segment.json"
        return self._request("get", location, params={"id": id_})

    def create_segment(self):
        location = "/api/v2/remarketing/segments.json"
        data = json.dumps(segment)
        return self._request("post", location, data=data)

    def delete_segment(self, id_=None):
        data = json.dumps([{"source_id": id_, "source_type": "segment"}])
        location = "/api/v1/remarketing/mass_action/delete.json"
        return self._request("post", location, data=data, expected_status=200, jsonify=True)

    def create_campaign(self):
        campaign["banners"][0]["urls"]["primary"]["id"] = self.get_url_id()
        campaign["banners"][0]["content"]["image_240x400"]["id"] = self.get_image_id()
        data = json.dumps(campaign)
        location = "/api/v2/campaigns.json"
        return self._request("post", location, data=data)

    def delete_campaign(self, id_=None):
        data = json.dumps([{"id": id_, "status": "deleted"}])
        location = "/api/v2/campaigns/mass_action.json"
        return self._request("post", location, data=data, expected_status=204, jsonify=False)

    def get_deleted_campaigns(self):
        location = "/api/v2/campaigns.json?_status=deleted"
        result = self._request("get", location)
        return [item['id'] for item in result['items']]

    def get_image_id(self):
        try:
            files = {
                "file": open('homework-3/sources/target.jpg', 'rb')
            }
        except FileNotFoundError:
            files = {
                "file": open('../sources/target.jpg', 'rb')
            }
        load_data = {"width": 0, "height": 0}
        load_location = "/api/v2/content/static.json"
        load_request = self._request("post", load_location, files=files, data=load_data)

        return load_request["id"]

    def get_url_id(self):
        location = "/api/v1/urls/"
        url_param = {"url": r"https://www.youtube.com/"}
        req = self._request("get", location, params=url_param)
        return req["id"]

    def get_csrf(self):
        res = self._request("get", "https://target.my.com/csrf/", jsonify=False)
        self.csrf_token = res.cookies.get("csrftoken")

    def _authorize(self):
        data = {
            "email": self.user,
            "password": self.password,
            "continue": "https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email",
            "failure": "https://account.my.com/login/"
        }

        self._request("POST", "https://auth-ac.my.com/auth?lang=ru&nosavelogin=0",
                      headers=self.auth_headers,
                      data=data, jsonify=False)
        self.get_csrf()
        logger.info("Logged in")
