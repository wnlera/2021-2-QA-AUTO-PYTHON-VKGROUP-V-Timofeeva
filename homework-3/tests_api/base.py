import pytest


class ApiBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

    @pytest.fixture(scope='function')
    def create_then_delete_campaign(self):
        resp = self.api_client.create_campaign()
        yield resp["id"]
        self.api_client.delete_campaign(resp["id"])
