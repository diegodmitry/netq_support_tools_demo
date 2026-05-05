import re
from html import escape, unescape
from dataclasses import dataclass
from urllib.parse import quote
from xml.dom import minidom
from xml.parsers.expat import ExpatError

from app.core.config import Settings, get_settings
from app.domain.audit_logs.schemas import NetqRecord, PayloadView
from app.infrastructure.http.client import IntegrationHttpClient
from app.infrastructure.http.errors import (
    IntegrationHTTPStatusError,
    IntegrationTimeoutError,
    IntegrationTransportError,
)


@dataclass
class AuditRecordDetail:
    payload: PayloadView


@dataclass
class AuditRecord:
    order_id: str
    order_type: str
    audit_payload: PayloadView
    mongo_payload: PayloadView
    related_order_ids: list[str]

    def to_model(self) -> NetqRecord:
        return NetqRecord(
            orderId=self.order_id,
            orderType=self.order_type,
            auditPayload=self.audit_payload,
            mongoPayload=self.mongo_payload,
            relatedOrderIds=self.related_order_ids,
        )


class AuditUpstreamError(Exception):
    def __init__(self, code: str, message: str, details: dict[str, str] | None = None) -> None:
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class EmptyAuditResultError(Exception):
    pass


class AuditLogsGateway:
    def __init__(self, settings: Settings, http_client: IntegrationHttpClient) -> None:
        self.settings = settings
        self.http_client = http_client

    def query_netq(self, *, environment: str, query_value: str) -> list[AuditRecord]:
        records: list[AuditRecord] = []
        queue = [query_value]
        visited: set[str] = set()

        while queue:
            order_id = queue.pop(0)
            if order_id in visited:
                continue
            visited.add(order_id)

            audit_payload = self._fetch_audit_netq_payload(
                environment=environment,
                order_id=order_id,
            )
            mongo_payload = self._fetch_mongo_netq_payload(
                environment=environment,
                order_id=order_id,
            )
            related_order_ids = self._extract_related_orders(mongo_payload.raw, order_id)
            records.append(
                AuditRecord(
                    order_id=order_id,
                    order_type=self._extract_order_type(mongo_payload.raw),
                    audit_payload=audit_payload,
                    mongo_payload=mongo_payload,
                    related_order_ids=related_order_ids,
                )
            )

            for related_order_id in related_order_ids:
                if related_order_id not in visited:
                    queue.append(related_order_id)

        if not records:
            raise EmptyAuditResultError

        return records

    def query_external(
        self,
        *,
        environment: str,
        query_type: str,
        query_value: str,
    ) -> AuditRecordDetail:
        base_url = self._audit_base_url(environment)
        encoded_value = quote(query_value, safe="")
        if environment == "prod":
            encoded_value = query_value

        payload = self._request_payload(
            url=f"{base_url}{query_type}/{encoded_value}",
            use_basic_auth=self.settings.audit_prod_basic_auth_enabled,
            auth_user=self.settings.audit_prod_basic_auth_user,
            auth_password=self.settings.audit_prod_basic_auth_pass_value,
            system=f"audit-{environment}",
            query_type=query_type,
        )
        return AuditRecordDetail(payload=payload)

    def query_sapa(self, query_value: str) -> AuditRecordDetail:
        payload = self._request_payload(
            url=f"{self._require(self.settings.sapa_url, 'SAPA URL')}{query_value}",
            use_basic_auth=self.settings.audit_prod_basic_auth_enabled,
            auth_user=self.settings.audit_prod_basic_auth_user,
            auth_password=self.settings.audit_prod_basic_auth_pass_value,
            system="sapa",
            query_type="SAPA",
        )
        return AuditRecordDetail(payload=payload)

    def query_related_detail(
        self,
        *,
        environment: str,
        order_id: str,
        panel: str,
    ) -> AuditRecordDetail:
        if panel == "left":
            payload = self._fetch_mongo_netq_payload(
                environment=environment,
                order_id=order_id,
            )
        else:
            payload = self._fetch_audit_netq_payload(
                environment=environment,
                order_id=order_id,
            )
        return AuditRecordDetail(payload=payload)

    def _fetch_audit_netq_payload(self, *, environment: str, order_id: str) -> PayloadView:
        return self._request_payload(
            url=f"{self._audit_base_url(environment)}{order_id}{self.settings.aux_url_audit}",
            use_basic_auth=self.settings.audit_prod_basic_auth_enabled,
            auth_user=self.settings.audit_prod_basic_auth_user,
            auth_password=self.settings.audit_prod_basic_auth_pass_value,
            system=f"audit-{environment}",
            query_type="NETQ",
        )

    def _fetch_mongo_netq_payload(self, *, environment: str, order_id: str) -> PayloadView:
        return self._request_payload(
            url=f"{self._mongo_base_url(environment)}{order_id}{self.settings.aux_url}",
            use_basic_auth=self.settings.mongo_prod_basic_auth_enabled,
            auth_user=self.settings.mongo_prod_basic_auth_user,
            auth_password=self.settings.mongo_prod_basic_auth_pass_value,
            system=f"mongo-{environment}",
            query_type="NETQ",
        )

    def _request_payload(
        self,
        *,
        url: str,
        use_basic_auth: bool,
        auth_user: str | None,
        auth_password: str | None,
        system: str,
        query_type: str,
    ) -> PayloadView:
        auth = None
        if use_basic_auth and auth_user and auth_password:
            auth = (auth_user, auth_password)

        try:
            response = self.http_client.request(
                method="GET",
                url=url,
                auth=auth,
            )
        except IntegrationTimeoutError as exc:
            raise AuditUpstreamError(
                code="UPSTREAM_TIMEOUT",
                message="Timeout while querying upstream service.",
                details={"system": system, "queryType": query_type},
            ) from exc
        except IntegrationHTTPStatusError as exc:
            raise AuditUpstreamError(
                code="UPSTREAM_HTTP_ERROR",
                message="Upstream service returned an unexpected status.",
                details={
                    "system": system,
                    "queryType": query_type,
                    "statusCode": str(exc.status_code),
                },
            ) from exc
        except IntegrationTransportError as exc:
            raise AuditUpstreamError(
                code="UPSTREAM_TRANSPORT_ERROR",
                message="Failed to reach upstream service.",
                details={"system": system, "queryType": query_type},
            ) from exc

        if not response.body:
            raise EmptyAuditResultError

        content_type = response.headers.get("content-type", "application/xml").split(";")[0]
        return PayloadView(
            contentType=content_type,
            raw=response.body,
            formatted=self._format_payload(response.body),
        )

    def _audit_base_url(self, environment: str) -> str:
        if environment == "prod":
            return self._require(self.settings.audit_prod_url, "Audit prod URL")
        return self._require(self.settings.audit_qa_url, "Audit QA URL")

    def _mongo_base_url(self, environment: str) -> str:
        if environment == "prod":
            return self._require(self.settings.mongo_prod_url, "Mongo prod URL")
        return self._require(self.settings.mongo_qa_url, "Mongo QA URL")

    @staticmethod
    def _extract_related_orders(response_body: str, current_order_id: str) -> list[str]:
        matches = re.findall(r"<order><id>([\w\-]+)</id>", response_body)
        return [order_id for order_id in matches if order_id != current_order_id]

    @staticmethod
    def _extract_order_type(response_body: str) -> str:
        match = re.search(r"<orderType>(.+?)</orderType>.+?priority", response_body, re.DOTALL)
        return match.group(1) if match else "UNKNOWN"

    @staticmethod
    def _format_payload(payload: str) -> str:
        outer_xml = AuditLogsGateway._try_pretty_xml(payload)
        if outer_xml is None:
            return payload

        return AuditLogsGateway._format_embedded_xml_sections(outer_xml)

    @staticmethod
    def _try_pretty_xml(payload: str) -> str | None:
        try:
            parsed = minidom.parseString(payload.encode("utf-8"))
            pretty_xml = parsed.toprettyxml(indent="  ")
        except (ExpatError, UnicodeEncodeError):
            return None

        return "\n".join(line.rstrip() for line in pretty_xml.splitlines() if line.strip())

    @staticmethod
    def _format_embedded_xml_sections(payload: str) -> str:
        section_pattern = re.compile(
            r"(?P<indent>^[ \t]*)<(?P<tag>requestPayload|responsePayload)>(?P<body>.*?)"
            r"</(?P=tag)>",
            re.MULTILINE | re.DOTALL,
        )

        def replace_section(match: re.Match[str]) -> str:
            indent = match.group("indent")
            tag = match.group("tag")
            body = match.group("body").strip()
            decoded_body = unescape(body).strip()
            formatted_body = AuditLogsGateway._try_pretty_xml(decoded_body)

            if formatted_body is None:
                return match.group(0)

            inner_indent = f"{indent}  "
            escaped_body = escape(formatted_body, quote=True)
            indented_body = "\n".join(
                f"{inner_indent}{line}" if line else inner_indent
                for line in escaped_body.splitlines()
            )

            return f"{indent}<{tag}>\n{indented_body}\n{indent}</{tag}>"

        return section_pattern.sub(replace_section, payload)

    @staticmethod
    def _require(value: str | None, label: str) -> str:
        if not value:
            raise AuditUpstreamError(
                code="AUDIT_CONFIGURATION_ERROR",
                message=f"{label} is not configured.",
            )
        return value


def build_audit_logs_gateway() -> AuditLogsGateway:
    settings = get_settings()
    return AuditLogsGateway(settings, IntegrationHttpClient(settings))
