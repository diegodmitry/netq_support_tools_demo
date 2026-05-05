from app.core.config import Settings
from app.infrastructure.sigra.soap_client import SigraSoapClient


class FakeHttpClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def request(self, **kwargs):
        self.calls.append(kwargs)
        return type(
            "ResponsePayload",
            (),
            {
                "status_code": 200,
                "body": "<soap:Envelope><soap:Body><ok/></soap:Body></soap:Envelope>",
            },
        )()


def test_sigra_soap_client_builds_request_and_calls_http_client() -> None:
    settings = Settings(
        _env_file=None,
        sigra_url="https://sigra.example/service",
        sigra_action="https://sigra.example/action",
        sigra_app="NETQ",
        sigra_code_app="99",
        sigra_timeout_seconds=30,
    )
    http_client = FakeHttpClient()
    client = SigraSoapClient(settings, http_client)

    result = client.call("ABC123")

    assert result.status_code == 200
    assert "ABC123" in result.request_xml
    assert "<get:Aplicacao>NETQ</get:Aplicacao>" in result.request_xml
    assert http_client.calls[0]["method"] == "POST"
    assert http_client.calls[0]["url"] == "https://sigra.example/service"
    assert http_client.calls[0]["headers"]["SOAPAction"] == "https://sigra.example/action"


def test_sigra_soap_client_requires_configuration() -> None:
    settings = Settings(
        _env_file=None,
        sigra_url=None,
        sigra_action=None,
        sigra_app="NETQ",
        sigra_code_app="99",
    )
    client = SigraSoapClient(settings, FakeHttpClient())

    try:
        client.call("ABC123")
    except ValueError as exc:
        assert "SIGRA URL" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing SIGRA configuration")
