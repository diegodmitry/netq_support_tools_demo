# Audit Logs Request Evidence

## Case

- `module-load`

## Date

- 2026-03-18 16:34:10 GMT

## Source action

- Click `Audit Logs` from the main menu

## Legacy screen

- `screenshots/after_click_Audit_Logs.png`
- `screenshots/full_screen_Audit_Logs.png`

## Request target

- `GET /netqLogs.jsp`

## Request parameters

```text
none
```

## Request metadata

- URL: `https://ossmanager.telecom.pt/NetqTools/netqLogs.jsp`
- Method: `GET`
- Status observed for this request: `200 OK`
- Remote address: `10.131.43.132:443`
- Referrer policy: `strict-origin-when-cross-origin`

## Real captured request

```http
GET /NetqTools/netqLogs.jsp HTTP/1.1
Host: ossmanager.telecom.pt
Referer: https://ossmanager.telecom.pt/NetqTools/menu.jsp
Cookie: JSESSIONID=617B76A761ECCC14679B7B9DFBFC34C3
X-Requested-With: XMLHttpRequest
Accept: text/html, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0
sec-ch-ua: "Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
```

## Notes

- This request loads the Audit Logs module shell only.
- It is not yet the main `NETQ` search request.
