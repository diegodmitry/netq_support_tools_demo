type AuditLogsQueryPayload = {
  environment: "prod" | "qa";
  queryType: "NETQ" | "TIBCO" | "NETWIN" | "SIGRA" | "NA" | "SAPA";
  queryValue: string;
  source: "request-id" | "sapa-id";
};

type AuditPayloadView = {
  contentType: string;
  formatted: string;
  raw: string;
};

type NetqRecord = {
  orderId: string;
  orderType: string;
  auditPayload: AuditPayloadView;
  mongoPayload: AuditPayloadView;
  relatedOrderIds: string[];
};

type NetqQueryResponse = {
  query: AuditLogsQueryPayload;
  mode: "netq";
  result: {
    rootOrderId: string;
    records: NetqRecord[];
  };
  meta: {
    generatedAt: string;
    requestId: string;
    totalRecords: number;
  };
};

function xmlPayload(formatted: string): AuditPayloadView {
  return {
    contentType: "application/xml",
    formatted,
    raw: formatted,
  };
}

const rootOrderId = "461bddc6-c5fd-4cb2-95eb-ce2932d06a9b";

const rootMongoPayload = `<?xml version="1.0" ?>
<order>
  <id>461bddc6-c5fd-4cb2-95eb-ce2932d06a9b</id>
  <orderType>ASSEMBLER_DALL</orderType>
  <priority>50</priority>
  <sessionId>69588883-9d95-4ca9-abff-124c68afe915</sessionId>
  <origin>WEB</origin>
  <originOrderId>3d0aa905-c416-411b-a678-3df0d0e04493</originOrderId>
  <originTime>1775834339589</originTime>
  <user>xid11185</user>
  <targetEntity>1700426781</targetEntity>
  <notificationParameters class="linked-hash-map">
    <param name="type">rest</param>
    <param name="partial">
      <boolean>true</boolean>
    </param>
    <param name="url">https://notifications.example.internal/netq/notifs</param>
  </notificationParameters>
  <orderParameters class="linked-hash-map">
    <param name="contexOperation">N</param>
    <param name="accountAccessId">1/1700426781</param>
    <param name="workflowId">java@b3df2ddc-d40f-4bc3-9645-9ee67c7756ca</param>
  </orderParameters>
  <state>FINISHED</state>
  <inventory class="pt.ptinovacao.netqpacks.model.assembler.inventory.DallInventory">
    <central>34AV01</central>
    <serviceId>1700426781</serviceId>
    <iptvId>502158555</iptvId>
    <ontModel>GR241AG</ontModel>
    <ponTechnology>GPON</ponTechnology>
  </inventory>
  <result class="pt.ptinovacao.netqpacks.model.assembler.result.DallResult">
    <platforms>
      <pt.ptinovacao.netqpacks.model.assembler.result.Platform>
        <name>CPEHN</name>
        <criticity>1</criticity>
      </pt.ptinovacao.netqpacks.model.assembler.result.Platform>
      <pt.ptinovacao.netqpacks.model.assembler.result.Platform>
        <name>MSIPTV</name>
        <criticity>1</criticity>
      </pt.ptinovacao.netqpacks.model.assembler.result.Platform>
      <pt.ptinovacao.netqpacks.model.assembler.result.Platform>
        <name>MPLS</name>
        <criticity>1</criticity>
      </pt.ptinovacao.netqpacks.model.assembler.result.Platform>
      <pt.ptinovacao.netqpacks.model.assembler.result.Platform>
        <name>VOIP</name>
        <criticity>0</criticity>
      </pt.ptinovacao.netqpacks.model.assembler.result.Platform>
    </platforms>
    <services>
      <pt.ptinovacao.netqpacks.model.assembler.result.Service>
        <name>NET</name>
        <type>SERVICE</type>
        <criticity>WARNING</criticity>
      </pt.ptinovacao.netqpacks.model.assembler.result.Service>
      <pt.ptinovacao.netqpacks.model.assembler.result.Service>
        <name>CPE</name>
        <type>NETWORK</type>
        <criticity>WARNING</criticity>
      </pt.ptinovacao.netqpacks.model.assembler.result.Service>
      <pt.ptinovacao.netqpacks.model.assembler.result.Service>
        <name>TV</name>
        <type>SERVICE</type>
        <criticity>WARNING</criticity>
      </pt.ptinovacao.netqpacks.model.assembler.result.Service>
    </services>
  </result>
</order>`;

const rootAuditPayload = `<?xml version="1.0" ?>
<info>no data about id: 461bddc6-c5fd-4cb2-95eb-ce2932d06a9b</info>`;

function record(
  orderId: string,
  orderType: string,
  mongoBody: string,
  auditBody: string,
  relatedOrderIds: string[] = [],
): NetqRecord {
  return {
    orderId,
    orderType,
    mongoPayload: xmlPayload(mongoBody),
    auditPayload: xmlPayload(auditBody),
    relatedOrderIds,
  };
}

const records: NetqRecord[] = [
  record(
    rootOrderId,
    "ASSEMBLER_DALL",
    rootMongoPayload,
    rootAuditPayload,
    [
      "b95f5f00-6d74-443d-b6ad-70d4e347f774",
      "ab514f9e-e188-476c-9abf-2f94016821b5",
      "13dc4760-a0cc-4a25-ab2b-6c3dd9501eb2",
      "af5b00f2-217a-4284-a31c-62cb28c7c633",
      "89662e06-43ec-4942-b291-3c7b7d7ac3a1",
    ],
  ),
  record(
    "b95f5f00-6d74-443d-b6ad-70d4e347f774",
    "INVENTORY_QUERY_NETWORK_ACCESS",
    `<?xml version="1.0" ?>
<inventory class="pt.ptinovacao.netqpacks.model.gpon.NetworkAccess">
  <id>1700426781</id>
  <central>34AV01</central>
  <serviceId>1700426781</serviceId>
  <accessType>RESIDENCIAL</accessType>
  <state>ACTIVE</state>
  <ont>
    <manufacturer>PTINOVACAO</manufacturer>
    <model>GR241AG</model>
    <serialNumber>5054494E91A01A7F</serialNumber>
    <technology>GPON</technology>
  </ont>
  <olt>
    <name>34AV01/65</name>
    <manufacturer>HUAWEI</manufacturer>
    <model>MA5800-X17</model>
    <ip>10.172.12.143</ip>
    <pon>1/2/4/15</pon>
  </olt>
</inventory>`,
    `<?xml version="1.0" ?>
<externalSystems>
  <system>Inventory</system>
  <requestId>b95f5f00-6d74-443d-b6ad-70d4e347f774</requestId>
  <latencyMs>725</latencyMs>
  <status>SUCCESS</status>
</externalSystems>`,
  ),
  record(
    "ab514f9e-e188-476c-9abf-2f94016821b5",
    "GPON_ESTADO_ONT",
    `<?xml version="1.0" ?>
<inventory class="pt.ptinovacao.netqpacks.model.gpon.inventory.GPONInventory">
  <id>1700426781</id>
  <central>34AV01</central>
  <networkAccess>
    <state>ACTIVE</state>
    <ont>
      <model>GR241AG</model>
      <softwareVersion>3HDMSW00000000</softwareVersion>
      <operState>ENABLED</operState>
    </ont>
    <olt>
      <name>34AV01/65</name>
      <model>MA5800-X17</model>
      <ponOperState>ENABLED</ponOperState>
    </olt>
  </networkAccess>
</inventory>`,
    `<?xml version="1.0" ?>
<externalSystems>
  <system>GPON</system>
  <requestId>ab514f9e-e188-476c-9abf-2f94016821b5</requestId>
  <status>SUCCESS</status>
  <message>CUSTOM_ADMIN_17: Acesso com Fibergateway GR241AG, GR141IG ou GR141DG</message>
  <message>CUSTOM_ADMIN_21: Modelo GR241AG</message>
</externalSystems>`,
  ),
  record(
    "13dc4760-a0cc-4a25-ab2b-6c3dd9501eb2",
    "MSIPTV_GET_OVERVIEW",
    `<?xml version="1.0" ?>
<result class="pt.ptinovacao.netqpacks.model.msiptv.result.OverviewResult">
  <accountId>502158555</accountId>
  <stbName>502158555_STB1</stbName>
  <messages>
    <message>
      <errorCode>MSIPTV_16</errorCode>
      <description>Pode ver 4 canais ou VODs, 4 dos quais em HD</description>
      <criticity>0</criticity>
    </message>
    <message>
      <errorCode>MSIPTV_19</errorCode>
      <description>Nenhuma STB possui menu de gravação activo</description>
      <criticity>1</criticity>
    </message>
    <message>
      <errorCode>MSIPTV_11</errorCode>
      <description>Oferta Base de Canais inconsistente em iESF</description>
      <criticity>1</criticity>
    </message>
  </messages>
</result>`,
    `<?xml version="1.0" ?>
<externalSystems>
  <system>MSIPTV</system>
  <requestId>13dc4760-a0cc-4a25-ab2b-6c3dd9501eb2</requestId>
  <status>WARNING</status>
  <endpoint>/msiptv/overview</endpoint>
</externalSystems>`,
  ),
  record(
    "af5b00f2-217a-4284-a31c-62cb28c7c633",
    "VOIP_QUERY_SIP_AS",
    `<?xml version="1.0" ?>
<result class="pt.ptinovacao.netqpacks.model.voip.result.sipas.SIPASResult">
  <voips>
    <pt.ptinovacao.netqpacks.model.voip.result.sipas.SIPASInfo>
      <naResponse>
        <code>IMS_00000</code>
        <response>Operacao realizada com sucesso</response>
      </naResponse>
      <serviceProvider>
        <id>vMTAS-FR:PT_COM</id>
        <phoneNumber>234383389</phoneNumber>
      </serviceProvider>
      <user>
        <id>sip:+351234383389@sip.sapo.pt</id>
        <phoneNumber>234383389</phoneNumber>
      </user>
    </pt.ptinovacao.netqpacks.model.voip.result.sipas.SIPASInfo>
  </voips>
</result>`,
    `<?xml version="1.0" ?>
<externalSystems>
  <system>VOIP</system>
  <requestId>af5b00f2-217a-4284-a31c-62cb28c7c633</requestId>
  <status>SUCCESS</status>
  <endpoint>/voip/query/sip-as</endpoint>
</externalSystems>`,
  ),
  record(
    "89662e06-43ec-4942-b291-3c7b7d7ac3a1",
    "RADIUS_QUERY",
    `<?xml version="1.0" ?>
<result class="pt.ptinovacao.netqpacks.model.radius.result.QueryResult">
  <naResponse>
    <code>RAD_000</code>
    <response>Operation successful</response>
  </naResponse>
  <onlineEntries>
    <pt.ptinovacao.netqpacks.model.radius.result.OnlineAuthenticationEntry>
      <tipoAcesso>GPON</tipoAcesso>
      <ipCliente>2.81.211.3</ipCliente>
      <macAddress>00:06:91:A0:1A:7F</macAddress>
      <data>2026-04-10 14:22:16</data>
      <contaCliente>as3579956b@3p.sapo.pt</contaCliente>
      <lineId>1700426781</lineId>
    </pt.ptinovacao.netqpacks.model.radius.result.OnlineAuthenticationEntry>
  </onlineEntries>
</result>`,
    `<?xml version="1.0" ?>
<externalSystems>
  <system>RADIUS</system>
  <requestId>89662e06-43ec-4942-b291-3c7b7d7ac3a1</requestId>
  <status>SUCCESS</status>
  <endpoint>/radius/query</endpoint>
</externalSystems>`,
  ),
];

export function buildNetqMockQueryResponse(
  payload: AuditLogsQueryPayload,
): NetqQueryResponse {
  return {
    query: payload,
    mode: "netq",
    result: {
      rootOrderId,
      records,
    },
    meta: {
      generatedAt: new Date().toISOString(),
      requestId: "mock-netq-request-id",
      totalRecords: records.length,
    },
  };
}
