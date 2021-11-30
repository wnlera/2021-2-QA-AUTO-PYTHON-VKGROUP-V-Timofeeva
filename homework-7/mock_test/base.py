import pytest
import random


class ApiBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

    def get_random_string(self, min_length=1, max_length=8, use_ru=False):
        _en_range = (97, 122)
        _ru_range = (1072, 1103)
        _rng = _ru_range if use_ru else _en_range
        length = random.randint(min_length, max_length)
        res = "".join([chr(random.randint(*_rng)) for _ in range(length)])
        res = res.lower().capitalize()
        return res
