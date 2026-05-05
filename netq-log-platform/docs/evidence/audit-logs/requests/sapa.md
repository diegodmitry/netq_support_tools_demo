# Audit Logs Request Evidence

## Case

- `sapa`

## Date

- 2026-03-18 16:42:36 GMT

## Source action

- Submit SAPA ID search

## Legacy screen

- `screenshots/submit_sapa_xml.png`

## Request target

- `POST /URLRequest`

## Request parameters

```text
id=1700426781
req=sapa
tid=sapa
chld=0
```

## Request metadata

- URL: `https://ossmanager.telecom.pt/NetqTools/URLRequest`
- Method: `POST`
- Status observed for this request: `200 OK`
- Remote address: `10.131.43.132:443`
- Referrer policy: `strict-origin-when-cross-origin`

## Real captured request

```http
POST /NetqTools/URLRequest HTTP/1.1
Host: ossmanager.telecom.pt
Origin: https://ossmanager.telecom.pt
Referer: https://ossmanager.telecom.pt/NetqTools/menu.jsp
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 38
Cookie: JSESSIONID=617B76A761ECCC14679B7B9DFBFC34C3
X-Requested-With: XMLHttpRequest
Accept: */*
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

- This is the SAPA submit flow from inside Audit Logs.
- The browser capture confirms `req=sapa`, `tid=sapa` and `chld=0`.
- Captured SAPA identifier: `1700426781`
