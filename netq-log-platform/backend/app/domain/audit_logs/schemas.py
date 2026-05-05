from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field

Environment = Literal["prod", "qa"]
QueryType = Literal["NETQ", "TIBCO", "NETWIN", "SIGRA", "NA", "SAPA"]
QuerySource = Literal["request-id", "sapa-id"]
ResultMode = Literal["netq", "external", "sapa"]
DetailPanel = Literal["left", "right"]


class PayloadView(BaseModel):
    contentType: str
    formatted: str
    raw: str


class AuditLogsQueryRequest(BaseModel):
    environment: Environment
    queryType: QueryType
    queryValue: str = Field(min_length=1)
    source: QuerySource = "request-id"


class AuditLogsQuerySummary(BaseModel):
    environment: Environment
    queryType: QueryType
    queryValue: str
    source: QuerySource


class NetqRecord(BaseModel):
    orderId: str
    orderType: str
    auditPayload: PayloadView
    mongoPayload: PayloadView
    relatedOrderIds: list[str]


class NetqResult(BaseModel):
    rootOrderId: str
    records: list[NetqRecord]


class ExternalResult(BaseModel):
    externalSystem: str
    externalId: str
    payload: PayloadView


class SapaResult(BaseModel):
    sapaId: str
    payload: PayloadView


class AuditLogsQueryMeta(BaseModel):
    generatedAt: datetime = Field(default_factory=lambda: datetime.now(UTC))
    requestId: str | None = None
    totalRecords: int | None = None


class AuditLogsQueryResponse(BaseModel):
    query: AuditLogsQuerySummary
    mode: ResultMode
    result: NetqResult | ExternalResult | SapaResult
    meta: AuditLogsQueryMeta


class RelatedDetailRequest(BaseModel):
    environment: Environment
    orderId: str = Field(min_length=1)
    panel: DetailPanel


class RelatedDetailQuerySummary(BaseModel):
    environment: Environment
    orderId: str
    panel: DetailPanel


class RelatedDetailResult(BaseModel):
    orderId: str
    panel: DetailPanel
    payload: PayloadView


class RelatedDetailResponse(BaseModel):
    query: RelatedDetailQuerySummary
    result: RelatedDetailResult
    meta: AuditLogsQueryMeta


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, str] | None = None


class AuditLogsErrorResponse(BaseModel):
    error: ErrorDetail
    meta: AuditLogsQueryMeta
