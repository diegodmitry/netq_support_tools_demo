from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.application.audit_logs.service import AuditLogsService, get_audit_logs_service
from app.domain.audit_logs.schemas import (
    AuditLogsErrorResponse,
    AuditLogsQueryRequest,
    AuditLogsQueryResponse,
    RelatedDetailRequest,
    RelatedDetailResponse,
)

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])
AuditLogsServiceDep = Annotated[AuditLogsService, Depends(get_audit_logs_service)]


@router.post(
    "/query",
    response_model=AuditLogsQueryResponse,
    responses={
        404: {"model": AuditLogsErrorResponse},
        502: {"model": AuditLogsErrorResponse},
    },
)
def query_audit_logs(
    payload: AuditLogsQueryRequest,
    request: Request,
    service: AuditLogsServiceDep,
) -> AuditLogsQueryResponse:
    return service.query(payload, request)


@router.post(
    "/related-detail",
    response_model=RelatedDetailResponse,
    responses={
        404: {"model": AuditLogsErrorResponse},
        502: {"model": AuditLogsErrorResponse},
    },
)
def query_related_detail(
    payload: RelatedDetailRequest,
    request: Request,
    service: AuditLogsServiceDep,
) -> RelatedDetailResponse:
    return service.query_related_detail(payload, request)
