import pytest

from base import ApiBase


class TestApi(ApiBase):

    @pytest.mark.API
    def test_create_campaign(self, create_then_delete_campaign):
        assert create_then_delete_campaign > 0

    @pytest.mark.API
    def test_create_segment(self):
        segment_id = self.create_segment()
        assert self.get_segment(segment_id)

    @pytest.mark.API
    def test_delete_segment(self):
        segment_id = self.create_segment()
        delete_result = self.delete_segment(segment_id)
        assert delete_result["successes"][0]["source_id"] == segment_id
