# Audit Logs Response Evidence

## Case

- `related-detail-right`

## Date

- 2026-03-18 16:55:55 GMT

## Expected legacy behavior

- Return formatted audit payload for the selected related order

## Observed response

```html
<pre><code class="hljs" ID="c101019e-6ccd-43f4-8bf3-5110fc6a15b9">&lt;?xml version="1.0" encoding="UTF-8"?>
&lt;list>
  &lt;pt.ptinovacao.netq.plugin.audit.model.AuditData>
    &lt;id>69bad8004ab57e07f70722fa&lt;/id>
    &lt;aggregatorId>c101019e-6ccd-43f4-8bf3-5110fc6a15b9&lt;/aggregatorId>
    &lt;system>NETWIN&lt;/system>
    &lt;operation>POST&lt;/operation>
    ...
    &lt;targetAddress>http://ptesb.telecom.pt:15000/PTP/25_RESOURCE/ResourceNetwork/Services/1.0/getAccessNetwork&lt;/targetAddress>
    &lt;success>true&lt;/success>
  &lt;/pt.ptinovacao.netq.plugin.audit.model.AuditData>
  &lt;pt.ptinovacao.netq.plugin.audit.model.AuditData>
    &lt;id>69bad8114ab57e07f70728aa&lt;/id>
    &lt;aggregatorId>c101019e-6ccd-43f4-8bf3-5110fc6a15b9&lt;/aggregatorId>
    &lt;system>NA&lt;/system>
    &lt;operation>readErrorCounters&lt;/operation>
    ...
    &lt;responsePayload>...GPON_000...Operation Successful...&lt;/responsePayload>
    &lt;success>true&lt;/success>
  &lt;/pt.ptinovacao.netq.plugin.audit.model.AuditData>
&lt;/list>
</code></pre>
```

## Confirmed legacy behavior from this capture

- Right detail is loaded with `div=right`
- Response is HTML containing escaped XML inside `<pre><code class="hljs">`
- Right side returns the audit/external systems payload
- Payload is a list of audit entries related to the same aggregator id
- Captured systems include:
  - `NETWIN`
  - `NA`
- Captured operations include SOAP/HTTP request payloads and downstream success details
