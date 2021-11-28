import pytest

from tests_api.base import ApiBase


class TestApi(ApiBase):

    @pytest.mark.API
    def test_create_campaign(self, create_then_delete_campaign):
        assert create_then_delete_campaign > 0

    @pytest.mark.API
    def test_create_segment(self):
        resp = self.api_client.create_segment()
        assert self.api_client.get_segment(resp["id"])

    @pytest.mark.API
    def test_delete_segment(self):
        resp = self.api_client.create_segment()
        delete_result = self.api_client.delete_segment(resp["id"])
        assert len(delete_result["errors"]) == 0
        assert delete_result["successes"][0]["source_id"] == resp["id"]
