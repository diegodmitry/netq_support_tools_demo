# Auth Session Request Evidence

## Case

- `login-invalid`

## Date

- 2026-03-18 16:31:28 GMT

## Source action

- Submit login form with invalid or empty credentials

## Legacy screen

- `screenshots/login1.png`

## Request target

- `POST /login.do`

## Request parameters

```text
ldomain=<not captured in shared dump>
lusername=<not captured in shared dump>
lpassword=<redacted-or-empty>
```

## Request metadata

- URL: `https://ossmanager.telecom.pt/NetqTools/login.do`
- Method: `POST`
- Status observed for this request: `302 Found`
- Remote address: `10.131.43.132:443`
- Referrer policy: `strict-origin-when-cross-origin`

## Real captured request

```http
POST /NetqTools/login.do HTTP/1.1
Host: ossmanager.telecom.pt
Origin: https://ossmanager.telecom.pt
Referer: https://ossmanager.telecom.pt/NetqTools/index.jsp
Content-Type: application/x-www-form-urlencoded
Content-Length: 66
Cookie: JSESSIONID=617B76A761ECCC14679B7B9DFBFC34C3
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
