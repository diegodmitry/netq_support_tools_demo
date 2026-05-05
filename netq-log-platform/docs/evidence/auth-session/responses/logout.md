# Auth Session Response Evidence

## Case

- `logout`

## Date

- 2026-03-18 16:27:56 GMT

## Expected legacy behavior

- Invalidate session
- Remove matching session cookie
- Redirect to `index.jsp`

## Observed response

```http
HTTP/1.1 302 Found
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:27:56 GMT
Content-Type: text/html;charset=UTF-8
Content-Length: 0
Connection: keep-alive
Cache-Control: no-store
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Pragma: no-cache
Set-Cookie: JSESSIONID=617B76A761ECCC14679B7B9DFBFC34C3; Path=/NetqTools; HttpOnly
Location: index.jsp
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: GET, HEAD, OPTIONS
Access-Control-Allow-Origin: *
X-cache-bypass: 0
```

## Follow-up navigation evidence

- Browser immediately requested `GET /NetqTools/index.jsp`
- Captured metadata:
  - URL: `https://ossmanager.telecom.pt/NetqTools/index.jsp`
  - Method: `GET`
  - Status: `200 OK`
  - Remote address: `10.131.43.132:443`
  - Referrer policy: `strict-origin-when-cross-origin`
- Relevant response:

```http
HTTP/1.1 200 OK
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:27:56 GMT
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

- Logout is triggered by `GET /logout.do`
- Server responds with redirect status `302`
- Redirect target is `index.jsp`
- Response sets no-cache headers:
  - `Cache-Control: no-store`
  - `Expires: Thu, 01 Jan 1970 00:00:00 GMT`
  - `Pragma: no-cache`
- Browser is redirected back to the login page successfully
- A new `JSESSIONID` is observed on the logout response path
