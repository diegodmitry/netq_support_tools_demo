import httpx

from app.core.config import Settings
from app.infrastructure.audit_logs.gateway import (
    AuditLogsGateway,
    AuditUpstreamError,
    EmptyAuditResultError,
)
from app.infrastructure.http.client import IntegrationHttpClient
from app.infrastructure.http.errors import IntegrationHTTPStatusError, IntegrationTimeoutError


def test_query_external_routes_to_audit_url_and_encodes_qa_hash() -> None:
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(200, text="<root />", headers={"content-type": "application/xml"})

    settings = Settings(
        _env_file=None,
        audit_prod_url="https://audit-prod.example/netq/audit/",
        audit_qa_url="https://audit-qa.example/netq/audit/",
    )
    gateway = AuditLogsGateway(
        settings,
        IntegrationHttpClient(
            settings,
            client=httpx.Client(transport=httpx.MockTransport(handler)),
        ),
    )

    result = gateway.query_external(
        environment="qa",
        query_type="SIGRA",
        query_value="ABC#123",
    )

    assert result.payload.contentType == "application/xml"
    assert seen_urls == ["https://audit-qa.example/netq/audit/SIGRA/ABC%23123"]


def test_query_netq_combines_audit_and_mongo_payloads() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if "audit-prod" in url:
            return httpx.Response(
                200,
                text="<audit><payload>ok</payload></audit>",
                headers={"content-type": "application/xml"},
            )
        return httpx.Response(
            200,
            text="""
            <root>
              <orderType>INSTALL</orderType>
              <priority>1</priority>
              <order><id>ORDER-123</id></order>
              <order><id>ORDER-456</id></order>
            </root>
            """,
            headers={"content-type": "application/xml"},
        )

    settings = Settings(
        _env_file=None,
        audit_prod_url="https://audit-prod.example/netq/audit/",
        mongo_prod_url="https://mongo-prod.example/netq/test/",
        aux_url="?related=true",
        aux_url_audit="?cache=true",
    )
    gateway = AuditLogsGateway(
        settings,
        IntegrationHttpClient(
            settings,
            client=httpx.Client(transport=httpx.MockTransport(handler)),
        ),
    )

    records = gateway.query_netq(environment="prod", query_value="ORDER-123")

    assert len(records) == 2
    assert records[0].order_id == "ORDER-123"
    assert records[0].order_type == "INSTALL"
    assert records[0].related_order_ids == ["ORDER-456"]


def test_query_sapa_routes_to_sapa_url() -> None:
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(
            200,
            text="<meo><servico id='1700426781' /></meo>",
            headers={"content-type": "application/xml"},
        )

    settings = Settings(
        _env_file=None,
        sapa_url="https://sapa.example/query?id_servico=",
    )
    gateway = AuditLogsGateway(
        settings,
        IntegrationHttpClient(
            settings,
            client=httpx.Client(transport=httpx.MockTransport(handler)),
        ),
    )

    result = gateway.query_sapa("1700426781")

    assert result.payload.contentType == "application/xml"
    assert result.payload.raw == "<meo><servico id='1700426781' /></meo>"
    assert seen_urls == ["https://sapa.example/query?id_servico=1700426781"]


def test_query_related_detail_left_routes_to_mongo_payload() -> None:
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(
            200,
            text="<order><id>ORDER-123</id></order>",
            headers={"content-type": "application/xml"},
        )

    settings = Settings(
        _env_file=None,
        mongo_prod_url="https://mongo-prod.example/netq/test/",
        aux_url="?related=true",
    )
    gateway = AuditLogsGateway(
        settings,
        IntegrationHttpClient(
            settings,
            client=httpx.Client(transport=httpx.MockTransport(handler)),
        ),
    )

    result = gateway.query_related_detail(
        environment="prod",
        order_id="ORDER-123",
        panel="left",
    )

    assert result.payload.raw == "<order><id>ORDER-123</id></order>"
    assert seen_urls == ["https://mongo-prod.example/netq/test/ORDER-123?related=true"]


def test_query_related_detail_right_routes_to_audit_payload() -> None:
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(
            200,
            text="<list><audit /></list>",
            headers={"content-type": "application/xml"},
        )

    settings = Settings(
        _env_file=None,
        audit_prod_url="https://audit-prod.example/netq/audit/",
        aux_url_audit="?cache=true",
    )
    gateway = AuditLogsGateway(
        settings,
        IntegrationHttpClient(
            settings,
            client=httpx.Client(transport=httpx.MockTransport(handler)),
        ),
    )

    result = gateway.query_related_detail(
        environment="prod",
        order_id="ORDER-123",
        panel="right",
    )

    assert result.payload.raw == "<list><audit /></list>"
    assert seen_urls == ["https://audit-prod.example/netq/audit/ORDER-123?cache=true"]


def test_query_external_raises_empty_result_for_blank_body() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="", headers={"content-type": "application/xml"})

    settings = Settings(
        _env_file=None,
        audit_prod_url="https://audit-prod.example/netq/audit/",
    )
    gateway = AuditLogsGateway(
        settings,
        IntegrationHttpClient(
            settings,
            client=httpx.Client(transport=httpx.MockTransport(handler)),
        ),
    )

    try:
        gateway.query_external(
            environment="prod",
            query_type="TIBCO",
            query_value="EXT-123",
        )
    except EmptyAuditResultError:
        assert True
    else:
        assert False, "Expected EmptyAuditResultError"


def test_query_external_maps_timeout_to_upstream_timeout_error() -> None:
    settings = Settings(
        _env_file=None,
        audit_prod_url="https://audit-prod.example/netq/audit/",
    )
    http_client = IntegrationHttpClient(settings)
    gateway = AuditLogsGateway(settings, http_client)

    def raise_timeout(**kwargs):
        raise IntegrationTimeoutError("timeout")

    http_client.request = raise_timeout  # type: ignore[method-assign]

    try:
        gateway.query_external(
            environment="prod",
            query_type="TIBCO",
            query_value="EXT-123",
        )
    except AuditUpstreamError as exc:
        assert exc.code == "UPSTREAM_TIMEOUT"
        assert exc.details == {"system": "audit-prod", "queryType": "TIBCO"}
    else:
        assert False, "Expected AuditUpstreamError"


def test_query_external_maps_http_status_error() -> None:
    settings = Settings(
        _env_file=None,
        audit_prod_url="https://audit-prod.example/netq/audit/",
    )
    http_client = IntegrationHttpClient(settings)
    gateway = AuditLogsGateway(settings, http_client)

    def raise_http_error(**kwargs):
        raise IntegrationHTTPStatusError(503, "unavailable")

    http_client.request = raise_http_error  # type: ignore[method-assign]

    try:
        gateway.query_external(
            environment="prod",
            query_type="TIBCO",
            query_value="EXT-123",
        )
    except AuditUpstreamError as exc:
        assert exc.code == "UPSTREAM_HTTP_ERROR"
        assert exc.details == {
            "system": "audit-prod",
            "queryType": "TIBCO",
            "statusCode": "503",
        }
    else:
        assert False, "Expected AuditUpstreamError"


def test_query_external_preserves_large_payload() -> None:
    large_segment = "A" * 12000
    large_xml = f"<root><payload>{large_segment}</payload></root>"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=large_xml,
            headers={"content-type": "application/xml"},
        )

    settings = Settings(
        _env_file=None,
        audit_prod_url="https://audit-prod.example/netq/audit/",
    )
    gateway = AuditLogsGateway(
        settings,
        IntegrationHttpClient(
            settings,
            client=httpx.Client(transport=httpx.MockTransport(handler)),
        ),
    )

    result = gateway.query_external(
        environment="prod",
        query_type="TIBCO",
        query_value="EXT-123",
    )

    assert result.payload.raw == large_xml
    assert large_segment in result.payload.formatted


def test_format_payload_pretty_prints_embedded_request_xml() -> None:
    payload = """
    <list>
      <AuditData>
        <requestPayload>&lt;Envelope&gt;&lt;Body&gt;&lt;Value&gt;123&lt;/Value&gt;&lt;/Body&gt;&lt;/Envelope&gt;</requestPayload>
      </AuditData>
    </list>
    """

    formatted = AuditLogsGateway._format_payload(payload)

    assert "<requestPayload>" in formatted
    assert "&lt;Envelope&gt;" in formatted
    assert "\n        &lt;Body&gt;" in formatted
    assert "\n          &lt;Value&gt;123&lt;/Value&gt;" in formatted


def test_format_payload_preserves_embedded_log_text_inside_response_xml() -> None:
    payload = """
    <list>
      <AuditData>
        <responsePayload>&lt;response&gt;&lt;log&gt;line 1

line 2&lt;/log&gt;&lt;/response&gt;</responsePayload>
      </AuditData>
    </list>
    """

    formatted = AuditLogsGateway._format_payload(payload)

    assert "&lt;response&gt;" in formatted
    assert "&lt;log&gt;line 1" in formatted
    assert "line 2&lt;/log&gt;" in formatted
    assert formatted.count("\n\n\n") == 0
