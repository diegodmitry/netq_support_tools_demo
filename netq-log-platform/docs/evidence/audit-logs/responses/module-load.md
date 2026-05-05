# Audit Logs Response Evidence

## Case

- `module-load`

## Date

- 2026-03-18 16:34:10 GMT

## Expected legacy behavior

- Load `netqLogs.jsp` into the main content area
- Show environment selector, ID type selector, ID field and SAPA field

## Observed response

```http
HTTP/1.1 200 OK
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:34:10 GMT
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

## Confirmed legacy behavior from this capture

- Audit Logs is loaded through `GET /netqLogs.jsp`
- The request is initiated asynchronously from `menu.jsp`
- The browser sends `X-Requested-With: XMLHttpRequest`
- Session cookie is required to access the module content

## Linked screenshots

- `screenshots/after_click_Audit_Logs.png`
- `screenshots/full_screen_Audit_Logs.png`

## Remaining evidence needed for `NETQ main`

- `POST /URLRequest`
- `req=prodMongo|qaMongo`
- `tid=NETQ`
- `chld=0`
- response HTML that builds the two-panel accordion view
