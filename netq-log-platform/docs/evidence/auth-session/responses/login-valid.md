# Auth Session Response Evidence

## Case

- `login-valid`

## Date

- 2026-03-18 16:15:43 GMT

## Expected legacy behavior

- Create authenticated session
- Store `LOGGED_USERNAME`
- Redirect to `menu.jsp`

## Observed response

```http
HTTP/1.1 302 Found
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:15:43 GMT
Content-Type: text/html;charset=UTF-8
Content-Length: 0
Connection: keep-alive
Set-Cookie: JSESSIONID=A94F187C0298522F5BF24FDBF345D153; Max-Age=28800; Expires=Thu, 19 Mar 2026 00:15:43 GMT
Location: menu.jsp
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: GET, HEAD, OPTIONS
Access-Control-Allow-Origin: *
X-cache-bypass: 0
```

## Follow-up navigation evidence

- Browser immediately requested `GET /NetqTools/menu.jsp`
- Captured metadata:
  - URL: `https://ossmanager.telecom.pt/NetqTools/menu.jsp`
  - Method: `GET`
  - Status: `200 OK`
  - Remote address: `10.131.43.132:443`
  - Referrer policy: `strict-origin-when-cross-origin`
- Relevant response headers:

```http
HTTP/1.1 200 OK
Server: nginx/1.20.0
Date: Wed, 18 Mar 2026 16:15:43 GMT
Content-Type: text/html;charset=UTF-8
Content-Encoding: gzip
Transfer-Encoding: chunked
Connection: keep-alive
Vary: Accept-Encoding
Access-Control-Allow-Headers: X-Requested-With
Access-Control-Allow-Methods: GET, HEAD, OPTIONS
Access-Control-Allow-Origin: *
X-cache-bypass: 0
```

## Confirmed legacy behavior from this capture

- Successful login returns redirect status `302`
- Redirect target is `menu.jsp`
- The server issues `JSESSIONID`
- Session cookie is returned with `Max-Age=28800`
- Authenticated navigation to `menu.jsp` succeeds with `200 OK`

## Linked screenshots

- `screenshots/after_login.png`
- `screenshots/side_menu.png`
