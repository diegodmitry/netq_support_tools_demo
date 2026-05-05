from dataclasses import dataclass
from datetime import datetime
from xml.dom import minidom
from xml.etree import ElementTree as ET

from app.core.config import Settings
from app.infrastructure.http.client import IntegrationHttpClient


@dataclass
class SigraSoapResult:
    request_xml: str
    response_xml: str
    status_code: int


class SigraSoapClient:
    def __init__(
        self,
        settings: Settings,
        http_client: IntegrationHttpClient,
    ) -> None:
        self.settings = settings
        self.http_client = http_client

    def call(self, ac: str) -> SigraSoapResult:
        request_xml = self.build_request_xml(ac)
        response = self.http_client.request(
            method="POST",
            url=self._require(self.settings.sigra_url, "SIGRA URL"),
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": self._require(self.settings.sigra_action, "SIGRA SOAPAction"),
            },
            content=request_xml,
            timeout_seconds=float(self.settings.sigra_timeout_seconds),
        )
        return SigraSoapResult(
            request_xml=request_xml,
            response_xml=response.body,
            status_code=response.status_code,
        )

    def build_request_xml(self, ac: str) -> str:
        envelope = ET.Element(
            "soapenv:Envelope",
            {
                "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
                "xmlns:soap": "urn://ptp.pt/SharedResources/SchemaDefinitions/EAIMessaging/SOAPHeader",
                "xmlns:_dat": "urn://ptp.pt/BusinessDomains/RESOURCE/ResourceNetwork/1.0/getNetworkInformation/_Data",
                "xmlns:get": "urn://ptp.pt/IntegrationDataModel/ResourceNetwork/1.0/getNetworkInformation",
            },
        )
        header = ET.SubElement(envelope, "soapenv:Header")
        header_request = ET.SubElement(header, "soap:HeaderRequest")
        ET.SubElement(header_request, "soap:npu").text = self._npu()
        ET.SubElement(header_request, "soap:creationTime").text = self._timestamp()
        ET.SubElement(header_request, "soap:timeout").text = str(
            self.settings.sigra_timeout_seconds
        )
        credentials = ET.SubElement(header_request, "soap:Credentials")
        ET.SubElement(credentials, "soap:systemCode").text = self._require(
            self.settings.sigra_code_app,
            "SIGRA code app",
        )

        body = ET.SubElement(envelope, "soapenv:Body")
        data_input = ET.SubElement(body, "_dat:DataInput")
        operation_input = ET.SubElement(data_input, "get:getNetworkInformationInput")
        params = ET.SubElement(operation_input, "get:ParametrosOperacao")
        ET.SubElement(params, "get:DataOperacao").text = self._timestamp()
        pedido = ET.SubElement(params, "get:PedidoInformacao")
        ET.SubElement(pedido, "get:Accao").text = "2"
        ET.SubElement(pedido, "get:AreaCentral").text = ac
        ET.SubElement(pedido, "get:Aplicacao").text = self._require(
            self.settings.sigra_app,
            "SIGRA app",
        )

        xml_bytes = ET.tostring(envelope, encoding="utf-8")
        return minidom.parseString(xml_bytes).toprettyxml(indent="  ")

    @staticmethod
    def _timestamp() -> str:
        return datetime.now().astimezone().isoformat(timespec="milliseconds")

    @staticmethod
    def _npu() -> str:
        return f"NETQ{datetime.now().strftime('%Y%m%d%H%M%S')}"

    @staticmethod
    def _require(value: str | None, label: str) -> str:
        if not value:
            raise ValueError(f"{label} is not configured.")
        return value
