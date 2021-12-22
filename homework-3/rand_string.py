import random

_en_range = (97, 122)
_ru_range = (1072, 1103)

random.seed(42)


def get_random_string(min_length=1, max_length=8, use_ru=False):
    _rng = _ru_range if use_ru else _en_range
    length = random.randint(min_length, max_length)
    res = "".join([chr(random.randint(*_rng)) for _ in range(length)])
    res = res.lower().capitalize()
    return res
