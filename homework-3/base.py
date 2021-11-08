import pytest


class ApiBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, logger):
        self.api_client = api_client
        self.logger = logger

    def create_campaign(self):
        resp = self.api_client.create_campaign()
        campaign_id = resp["id"]
        return campaign_id

    def delete_campaign(self, id_):
        return self.api_client.delete_campaign(id_)

    @pytest.fixture(scope='function')
    def create_then_delete_campaign(self):
        campaign_id = self.create_campaign()
        yield campaign_id
        self.delete_campaign(campaign_id)

    def create_segment(self):
        resp = self.api_client.create_segment()
        return resp["id"]

    def get_segment(self, id_):
        return self.api_client.get_segment(id_)

    def delete_segment(self, id_):
        resp = self.api_client.delete_segment(id_)
        return resp
