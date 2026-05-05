# Audit Logs Response Evidence

## Case

- `netq-main`

## Date

- 2026-03-18 16:52:23 GMT

## Expected legacy behavior

- Render two accordion columns
- Show left and right toggle buttons
- Create expandable related record sections

## Observed response

```http
HTTP/1.1 200 OK
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:52:23 GMT
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

## Response body summary

- The backend returns HTML, not JSON
- The top-level `NETQ` response renders:
  - button `<<` with id `btn-left`
  - button `>>` or toggled equivalent for right/left panel control
  - left accordion column for `Registo do pedido com o ID: ...`
  - right accordion column for `Pedidos a sistemas externos relacionado com o ID: ...`
  - hidden input `req=prodMongo`
- Clicking accordion items triggers follow-up `POST /URLRequest` calls with `chld=1`

## Confirmed legacy behavior from this capture

- Main `NETQ` lookup uses `POST /URLRequest`
- `req=prodMongo`, `tid=NETQ`, `chld=0`
- Successful top-level query returns `200 OK`
- The response builds a two-panel accordion UI, not a simple payload block
- Follow-up left/right detail requests are required to see payload contents

## Remaining evidence needed

- top-level HTML excerpt from the response body, if you want the rendered structure preserved verbatim
