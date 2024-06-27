import pytest
from unittest.mock import MagicMock, patch

from src.flask.router import validate_request_payload
from src.flask.types import OutcomeResponse

@patch("src.flask.router.request")
@pytest.mark.parametrize(
    "method_type, response", 
    [
        ("GET", None),
        ("PUT", None),
        ("DELETE", None),
        ("POST", OutcomeResponse(success=False))
    ]     
)
def test_validate_request_payload_method_type(mock_request: MagicMock, method_type: str, response: OutcomeResponse | None,) -> None:
    # Always send an erronous payload so we can see if it went through
    # next round of validation
    mock_request.endpoint.return_value = "test"
    mock_request.method.return_value = method_type
    assert validate_request_payload() == response