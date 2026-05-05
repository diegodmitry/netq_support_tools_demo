# Audit Logs Response Evidence

## Case

- `sapa`

## Date

- 2026-03-18 16:42:36 GMT

## Expected legacy behavior

- Render one formatted payload
- Show heading with queried SAPA id

## Observed response

```http
HTTP/1.1 200 OK
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:42:36 GMT
Content-Type: text/html;charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Vary: Accept-Encoding
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: GET, HEAD, OPTIONS
Access-Control-Allow-Origin: *
X-cache-bypass: 0
Content-Encoding: gzip
```

## Response body excerpt

```html
<h5>Consulta a sapa XML2 com ID: 1700426781</h5>
<pre><code class="hljs">&lt;?xml version="1.0" encoding="UTF-8"?>
&lt;meo>
  &lt;servicoSAPA idServicoSAPA="1">
    &lt;servicos>
      &lt;servico codigoEstado="2" estado="Em Servico" id="1700426781" subscriberId="5000" suporte="fibra" tipo="ACESSO">
        &lt;classeComercial codigo="C98" debitoDown="30000" debitoUp="3000"/>
        &lt;classeTecnica codigo="T189" debitoDown="1000000" debitoUp="400000"/>
      &lt;/servico>
      ...
    &lt;/servicos>
  &lt;/servicoSAPA>
&lt;/meo>
</code></pre>
```

## Confirmed legacy behavior from this capture

- SAPA submit calls `POST /URLRequest`
- The request is asynchronous and sends `X-Requested-With: XMLHttpRequest`
- Response content type is `text/html;charset=UTF-8`
- A successful SAPA query returns `200 OK`
- Rendered title is `Consulta a sapa XML2 com ID: 1700426781`
- Payload is returned as HTML containing escaped XML inside `<pre><code class="hljs">`
- Response includes the full SAPA XML payload for the queried service id

## Linked screenshots

- `screenshots/submit_sapa_xml.png`

## Remaining evidence needed

- none for the successful SAPA happy path represented by this capture
