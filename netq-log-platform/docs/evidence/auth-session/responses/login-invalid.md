# Auth Session Response Evidence

## Case

- `login-invalid`

## Date

- 2026-03-18 16:31:28 GMT

## Expected legacy behavior

- Redirect to `index.jsp?authFailed=true`
- Show `ERRO NA AUTENTICAÇÃO !!!`

## Observed response

```http
HTTP/1.1 302 Found
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:31:28 GMT
Content-Type: text/html;charset=UTF-8
Content-Length: 0
Connection: keep-alive
Location: index.jsp?authFailed=true
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: GET, HEAD, OPTIONS
Access-Control-Allow-Origin: *
X-cache-bypass: 0
```

## Follow-up navigation evidence

- Browser immediately requested `GET /NetqTools/index.jsp?authFailed=true`
- Captured metadata:
  - URL: `https://ossmanager.telecom.pt/NetqTools/index.jsp?authFailed=true`
  - Method: `GET`
  - Status: `200 OK`
  - Remote address: `10.131.43.132:443`
  - Referrer policy: `strict-origin-when-cross-origin`
- Relevant response:

```http
HTTP/1.1 200 OK
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:31:28 GMT
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

- Invalid login returns redirect status `302`
- Redirect target is `index.jsp?authFailed=true`
- Browser reloads the login page successfully with `200 OK`
- End-user error is expected to be shown on the login page after the redirect

## Linked screenshots

- `screenshots/login1.png`
