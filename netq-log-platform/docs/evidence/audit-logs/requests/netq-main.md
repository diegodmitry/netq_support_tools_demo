# Audit Logs Request Evidence

## Case

- `netq-main`

## Date

- 2026-03-18 16:52:23 GMT

## Source action

- Submit Audit Logs search for `NETQ`

## Legacy screen

- `screenshots/after_click_Audit_Logs.png`
- `screenshots/full_screen_Audit_Logs.png`

## Request target

- `POST /URLRequest`

## Request parameters

```text
id=c101019e-6ccd-43f4-8bf3-5110fc6a15b9
req=prodMongo
tid=NETQ
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
Content-Length: 69
Cookie: JSESSIONID=02D8A35813B971F94965B28A711AFFE7
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
