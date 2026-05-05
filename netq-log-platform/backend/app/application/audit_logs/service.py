from dataclasses import dataclass

from fastapi import Request, status

from app.core.observability import request_id_context
from app.domain.audit_logs.schemas import (
    AuditLogsErrorResponse,
    AuditLogsQueryMeta,
    AuditLogsQueryRequest,
    AuditLogsQueryResponse,
    AuditLogsQuerySummary,
    ExternalResult,
    NetqResult,
    RelatedDetailRequest,
    RelatedDetailResponse,
    RelatedDetailResult,
    RelatedDetailQuerySummary,
    SapaResult,
)
from app.domain.auth.errors import AuthAPIError
from app.infrastructure.audit_logs.gateway import (
    AuditLogsGateway,
    AuditRecord,
    AuditRecordDetail,
    AuditUpstreamError,
    EmptyAuditResultError,
    build_audit_logs_gateway,
)


@dataclass
class QueryResult:
    body: AuditLogsQueryResponse


class AuditLogsService:
    def __init__(self, gateway: AuditLogsGateway) -> None:
        self.gateway = gateway

    def query(self, payload: AuditLogsQueryRequest, request: Request) -> AuditLogsQueryResponse:
        try:
            if payload.queryType == "SAPA" or payload.source == "sapa-id":
                result = self.gateway.query_sapa(payload.queryValue)
                return self._build_sapa_response(payload, result)

            if payload.queryType == "NETQ":
                result = self.gateway.query_netq(
                    environment=payload.environment,
                    query_value=payload.queryValue,
                )
                return self._build_netq_response(payload, result)

            result = self.gateway.query_external(
                environment=payload.environment,
                query_type=payload.queryType,
                query_value=payload.queryValue,
            )
            return self._build_external_response(payload, result)
        except EmptyAuditResultError as exc:
            raise self._error(
                status.HTTP_404_NOT_FOUND,
                code="AUDIT_RESULT_EMPTY",
                message="No records were returned for the submitted query.",
                details={"queryValue": payload.queryValue},
            ) from exc
        except AuditUpstreamError as exc:
            raise self._error(
                status.HTTP_502_BAD_GATEWAY,
                code=exc.code,
                message=exc.message,
                details=exc.details,
            ) from exc

    def query_related_detail(
        self,
        payload: RelatedDetailRequest,
        request: Request,
    ) -> RelatedDetailResponse:
        try:
            result = self.gateway.query_related_detail(
                environment=payload.environment,
                order_id=payload.orderId,
                panel=payload.panel,
            )
            return RelatedDetailResponse(
                query=RelatedDetailQuerySummary(**payload.model_dump()),
                result=RelatedDetailResult(
                    orderId=payload.orderId,
                    panel=payload.panel,
                    payload=result.payload,
                ),
                meta=AuditLogsQueryMeta(requestId=request_id_context.get()),
            )
        except EmptyAuditResultError as exc:
            raise self._error(
                status.HTTP_404_NOT_FOUND,
                code="AUDIT_RESULT_EMPTY",
                message="No records were returned for the submitted query.",
                details={"orderId": payload.orderId, "panel": payload.panel},
            ) from exc
        except AuditUpstreamError as exc:
            raise self._error(
                status.HTTP_502_BAD_GATEWAY,
                code=exc.code,
                message=exc.message,
                details=exc.details,
            ) from exc

    def _build_netq_response(
        self,
        payload: AuditLogsQueryRequest,
        records: list[AuditRecord],
    ) -> AuditLogsQueryResponse:
        return AuditLogsQueryResponse(
            query=self._to_query_summary(payload),
            mode="netq",
            result=NetqResult(
                rootOrderId=payload.queryValue,
                records=[record.to_model() for record in records],
            ),
            meta=AuditLogsQueryMeta(
                requestId=request_id_context.get(),
                totalRecords=len(records),
            ),
        )

    def _build_external_response(
        self,
        payload: AuditLogsQueryRequest,
        record: AuditRecordDetail,
    ) -> AuditLogsQueryResponse:
        return AuditLogsQueryResponse(
            query=self._to_query_summary(payload),
            mode="external",
            result=ExternalResult(
                externalSystem=payload.queryType,
                externalId=payload.queryValue,
                payload=record.payload,
            ),
            meta=AuditLogsQueryMeta(requestId=request_id_context.get()),
        )

    def _build_sapa_response(
        self,
        payload: AuditLogsQueryRequest,
        record: AuditRecordDetail,
    ) -> AuditLogsQueryResponse:
        return AuditLogsQueryResponse(
            query=self._to_query_summary(payload),
            mode="sapa",
            result=SapaResult(
                sapaId=payload.queryValue,
                payload=record.payload,
            ),
            meta=AuditLogsQueryMeta(requestId=request_id_context.get()),
        )

    @staticmethod
    def _to_query_summary(payload: AuditLogsQueryRequest) -> AuditLogsQuerySummary:
        return AuditLogsQuerySummary(**payload.model_dump())

    def _error(
        self,
        status_code: int,
        *,
        code: str,
        message: str,
        details: dict[str, str] | None = None,
    ) -> AuthAPIError:
        body = AuditLogsErrorResponse(
            error={"code": code, "message": message, "details": details},
            meta=AuditLogsQueryMeta(requestId=request_id_context.get()),
        )
        return AuthAPIError(status_code=status_code, body=body.model_dump(exclude_none=True))


def get_audit_logs_service() -> AuditLogsService:
    return AuditLogsService(build_audit_logs_gateway())
