# Auth Session Request Evidence

## Case

- `login-valid`

## Date

- 2026-03-18 16:15:43 GMT

## Source action

- Submit login form with valid domain, username and password

## Legacy screen

- `screenshots/login.png`

## Request target

- `POST /login.do`

## Request parameters

```text
ldomain=ptportugal
lusername=xid11185
lpassword=<redacted>
```

## Notes

- Must correspond to an allowed user
- Must authenticate successfully in LDAP
- Real captured request:

```http
POST /NetqTools/login.do HTTP/1.1
Host: ossmanager.telecom.pt
Origin: https://ossmanager.telecom.pt
Referer: https://ossmanager.telecom.pt/NetqTools/index.jsp
Content-Type: application/x-www-form-urlencoded
Content-Length: 67
Cookie: JSESSIONID=A94F187C0298522F5BF24FDBF345D153
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0
sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

- Request metadata:
  - URL: `https://ossmanager.telecom.pt/NetqTools/login.do`
  - Method: `POST`
  - Status observed for this request: `302 Found`
  - Remote address: `10.131.43.132:443`
  - Referrer policy: `strict-origin-when-cross-origin`
- The browser capture supplied headers and transport metadata, but not the submitted form values themselves.
