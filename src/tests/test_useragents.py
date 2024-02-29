import time

from parserian.useragents import UserAgentRoller


def test_fetch():
    roller = UserAgentRoller()
    next = roller.next()
    assert roller.next()

