import logging
from urllib.parse import urljoin
import json

import requests

from const_campaign import campaign

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
            "Origin": "https://target.my.com",
            "Referer": "https://target.my.com/"
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

    def _request(self, method, location, headers=None, data=None, params=None, expected_status=(200,), jsonify=True):
        url = urljoin(self.base_url, location)
        self.log_before_request(url, headers, data, expected_status)
        headers = headers or self.headers
        response = self.session.request(method, url, headers=headers, data=data, params=params)
        self.log_after_request(response)

        if response.status_code not in expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.request} for URL "{url}"')

        if jsonify:
            json_response = response.json()
            return json_response
        return response

    def get_segment(self, id_=None):
        location = "/api/v2/coverage/segment.json"
        return self._request("get", location, params={"id": id_})

    def create_segment(self):
        location = "/api/v2/remarketing/segments.json?fields=relations__object_type,relations__object_id," \
                   "relations__params,relations__params__score,relations__id,relations_count,id,name,pass_condition," \
                   "created,campaign_ids,users,flags"
        data = json.dumps({"name": "Новый сегмент", "pass_condition": 1, "relations": [
            {"object_type": "remarketing_player", "params": {"type": "positive", "left": 365, "right": 0}}],
                           "logicType": "or"})
        return self._request("post", location, data=data)

    def delete_segment(self, id_=None):
        data = json.dumps([{"source_id": id_, "source_type": "segment"}])
        location = "/api/v1/remarketing/mass_action/delete.json"
        return self._request("post", location, data=data, expected_status=(200, 204), jsonify=True)

    def create_campaign(self):
        data = json.dumps(campaign)
        location = "/api/v2/campaigns.json"
        return self._request("post", location, data=data)

    def delete_campaign(self, id_=None):
        data = json.dumps([{"id": id_, "status": "deleted"}])
        location = "/api/v2/campaigns/mass_action.json"
        return self._request("post", location, data=data, expected_status=(200, 204), jsonify=False)

    def get_deleted_campaigns(self):
        location = "/api/v2/campaigns.json?_status=deleted"
        result = self._request("get", location)
        return [item['id'] for item in result['items']]

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
        res = self._request("get", "https://target.my.com/csrf/", jsonify=False)
        self.csrf_token = res.cookies.get("csrf_token") or res.cookies.get("csrftoken")
        logger.info("Logged in")
