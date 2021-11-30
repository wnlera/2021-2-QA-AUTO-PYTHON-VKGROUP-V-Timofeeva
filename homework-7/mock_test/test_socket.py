import pytest

from mock_test.base import ApiBase


class TestMock(ApiBase):

    @pytest.mark.mock
    def test_api_create_card(self):
        name = self.get_random_string(4, 10)
        resp = self.api_client.add_card(name)
        assert resp["name"] == name
        assert len(resp["number"]) > 10

    @pytest.mark.mock
    def test_api_get_card(self):
        name = self.get_random_string(4, 10)
        resp_create = self.api_client.add_card(name)
        card_id = resp_create["id"]
        resp = self.api_client.get_card(card_id)
        assert resp["name"] == name
        assert resp["number"] == resp_create["number"]

    @pytest.mark.mock
    def test_api_update_card(self):
        name = self.get_random_string(4, 10)
        resp_create = self.api_client.add_card(name)
        card_id = resp_create["id"]
        resp_get = self.api_client.get_card(card_id)
        old_number = resp_get["number"]
        resp = self.api_client.update_card(card_id, self.get_random_string())
        assert resp["number"] != old_number

    @pytest.mark.mock
    def test_api_delete_card(self):
        name = self.get_random_string(4, 10)
        resp_create = self.api_client.add_card(name)
        card_id = resp_create["id"]
        resp = self.api_client.delete_card(card_id)
        assert resp == f'Card with id "{card_id}" successfully deleted'
