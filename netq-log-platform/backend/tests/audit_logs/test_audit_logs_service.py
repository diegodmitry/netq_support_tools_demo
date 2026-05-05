import pytest
from unittest.mock import Mock

from app.application.audit_logs.service import AuditLogsService
from app.domain.audit_logs.schemas import AuditLogsQueryRequest, PayloadView, RelatedDetailRequest
from app.domain.auth.errors import AuthAPIError
from app.infrastructure.audit_logs.gateway import AuditRecordDetail
from app.infrastructure.audit_logs.gateway import AuditUpstreamError, EmptyAuditResultError


def test_service_routes_sapa_query_type_to_sapa_gateway() -> None:
    gateway = Mock()
    gateway.query_sapa.return_value = AuditRecordDetail(
        payload=PayloadView(
            contentType="application/xml",
            formatted="<formatted />",
            raw="<raw />",
        )
    )

    service = AuditLogsService(gateway)
    response = service.query(
        AuditLogsQueryRequest(
            environment="prod",
            queryType="SAPA",
            queryValue="1700426781",
            source="sapa-id",
        ),
        request=Mock(),
    )

    gateway.query_sapa.assert_called_once_with("1700426781")
    gateway.query_netq.assert_not_called()
    gateway.query_external.assert_not_called()
    assert response.mode == "sapa"
    assert response.result.sapaId == "1700426781"


def test_service_routes_sapa_source_to_sapa_gateway() -> None:
    gateway = Mock()
    gateway.query_sapa.return_value = AuditRecordDetail(
        payload=PayloadView(
            contentType="application/xml",
            formatted="<formatted />",
            raw="<raw />",
        )
    )

    service = AuditLogsService(gateway)
    response = service.query(
        AuditLogsQueryRequest(
            environment="qa",
            queryType="NETQ",
            queryValue="1700426781",
            source="sapa-id",
        ),
        request=Mock(),
    )

    gateway.query_sapa.assert_called_once_with("1700426781")
    gateway.query_netq.assert_not_called()
    gateway.query_external.assert_not_called()
    assert response.mode == "sapa"


def test_service_routes_related_detail_to_explicit_panel() -> None:
    gateway = Mock()
    gateway.query_related_detail.return_value = AuditRecordDetail(
        payload=PayloadView(
            contentType="application/xml",
            formatted="<formatted />",
            raw="<raw />",
        )
    )

    service = AuditLogsService(gateway)
    response = service.query_related_detail(
        RelatedDetailRequest(
            environment="prod",
            orderId="ORDER-123",
            panel="right",
        ),
        request=Mock(),
    )

    gateway.query_related_detail.assert_called_once_with(
        environment="prod",
        order_id="ORDER-123",
        panel="right",
    )
    assert response.result.orderId == "ORDER-123"
    assert response.result.panel == "right"


def test_service_maps_empty_query_result_to_404_error() -> None:
    gateway = Mock()
    gateway.query_external.side_effect = EmptyAuditResultError()
    service = AuditLogsService(gateway)

    with pytest.raises(AuthAPIError) as exc_info:
        service.query(
            AuditLogsQueryRequest(
                environment="prod",
                queryType="TIBCO",
                queryValue="EXT-123",
                source="request-id",
            ),
            request=Mock(),
        )

    assert exc_info.value.status_code == 404
    assert exc_info.value.body["error"]["code"] == "AUDIT_RESULT_EMPTY"


def test_service_maps_upstream_error_to_502_error() -> None:
    gateway = Mock()
    gateway.query_external.side_effect = AuditUpstreamError(
        code="UPSTREAM_TIMEOUT",
        message="Timeout while querying upstream service.",
        details={"system": "audit-prod", "queryType": "TIBCO"},
    )
    service = AuditLogsService(gateway)

    with pytest.raises(AuthAPIError) as exc_info:
        service.query(
            AuditLogsQueryRequest(
                environment="prod",
                queryType="TIBCO",
                queryValue="EXT-123",
                source="request-id",
            ),
            request=Mock(),
        )

    assert exc_info.value.status_code == 502
    assert exc_info.value.body["error"]["code"] == "UPSTREAM_TIMEOUT"
    assert exc_info.value.body["error"]["details"] == {
        "system": "audit-prod",
        "queryType": "TIBCO",
    }
