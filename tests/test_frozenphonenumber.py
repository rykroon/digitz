import pytest

from digitz import FrozenPhoneNumber


@pytest.fixture
def num_usa() -> FrozenPhoneNumber:
    return FrozenPhoneNumber.parse("+1 (201) 555-0123")


@pytest.fixture
def num_usa_toll_free():
    return FrozenPhoneNumber.parse("+1 (800) 234-5678")


@pytest.fixture
def num_usa_voip():
    return FrozenPhoneNumber.parse("+1 (305) 209-0123")


@pytest.fixture
def num_usa_invalid():
    return FrozenPhoneNumber.parse("+1 (201) 555-012")


@pytest.fixture
def num_can():
    return FrozenPhoneNumber.parse("+1 (506) 234-5678")


@pytest.fixture
def num_mex():
    return FrozenPhoneNumber.parse("+52 200 123 4567")