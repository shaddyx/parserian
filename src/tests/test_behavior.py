import time

from parserian.behavior import Behavior


def test_random_pause():
    b = Behavior()
    begin = time.time()
    b.random_pause(0.1, 0.2)
    end = time.time()
    assert end - begin >= 0.1
    assert end - begin <= 0.2

