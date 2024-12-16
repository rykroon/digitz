import pytest
import phonenumbers as pn
from digitz import PhoneNumber


USA_EXAMPLE_NUMBER = "+1 (201) 555-0123"
CAN_EXAMPLE_NUMBER = "+1 506-234-5678"
MEX_EXAMPLE_NUMBER = "+52 200 123 4567"
ITA_EXAMPLE_NUMBER = "+39 02 1234 5678"

USA_FIXED_LINE_EXAMPLE_NUMBER = "+1 201-555-0123"
USA_MOBILE_EXAMPLE_NUMBER = "+1 201-555-0123"
USA_TOLL_FREE_EXAMPLE_NUMBER = "+1 800-234-5678"
USA_VOIP_EXAMPLE_NUMBER = "+1 305-209-0123"
USA_INVALID_EXAMPLE_NUMBER = "+1 201555012"


@pytest.fixture
def num_usa() -> PhoneNumber:
    return PhoneNumber.parse(USA_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_pn() -> pn.PhoneNumber:
    return pn.parse(USA_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_toll_free() -> PhoneNumber:
    return PhoneNumber.parse(USA_TOLL_FREE_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_toll_free_pn() -> pn.PhoneNumber:
    return pn.parse(USA_TOLL_FREE_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_voip() -> PhoneNumber:
    return PhoneNumber.parse(USA_VOIP_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_voip_pn() -> pn.PhoneNumber:
    return pn.parse(USA_VOIP_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_invalid() -> PhoneNumber:
    return PhoneNumber.parse(USA_INVALID_EXAMPLE_NUMBER)


@pytest.fixture
def num_usa_invalid_pn() -> pn.PhoneNumber:
    return pn.parse(USA_INVALID_EXAMPLE_NUMBER)


@pytest.fixture
def num_can() -> PhoneNumber:
    return PhoneNumber.parse(CAN_EXAMPLE_NUMBER)


@pytest.fixture
def num_can_pn() -> pn.PhoneNumber:
    return pn.parse(CAN_EXAMPLE_NUMBER)


@pytest.fixture
def num_mex() -> PhoneNumber:
    return PhoneNumber.parse(MEX_EXAMPLE_NUMBER)


@pytest.fixture
def num_mex_pn() -> pn.PhoneNumber:
    return pn.parse(MEX_EXAMPLE_NUMBER)


@pytest.fixture
def num_ita() -> PhoneNumber:
    return PhoneNumber.parse(ITA_EXAMPLE_NUMBER)


@pytest.fixture
def num_ita_pn() -> pn.PhoneNumber:
    return pn.parse(ITA_EXAMPLE_NUMBER)
