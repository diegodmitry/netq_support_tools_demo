# Audit Logs Response Evidence

## Case

- `related-detail-left`

## Date

- 2026-03-18 16:54:12 GMT

## Expected legacy behavior

- Return formatted mongo payload for the selected related order

## Observed response

```html
<pre><code class="hljs" ID="c101019e-6ccd-43f4-8bf3-5110fc6a15b9">&lt;?xml version="1.0" encoding="UTF-8"?>
&lt;order>
  &lt;id>c101019e-6ccd-43f4-8bf3-5110fc6a15b9&lt;/id>
  &lt;orderType>GPON_ERROS_OPTICO_ONT&lt;/orderType>
  &lt;priority>50&lt;/priority>
  ...
  &lt;targetEntity>1700426781&lt;/targetEntity>
  ...
  &lt;state>FINISHED&lt;/state>
  ...
  &lt;result class="pt.ptinovacao.netqpacks.model.gpon.result.ErrosOpticosOntResult">
    &lt;naResponse>
      &lt;code>GPON_000&lt;/code>
      &lt;response>Operation Successful&lt;/response>
    &lt;/naResponse>
    ...
  &lt;/result>
&lt;/order>
</code></pre>
```

## Confirmed legacy behavior from this capture

- Left detail is loaded with `div=left`
- Response is HTML containing escaped XML inside `<pre><code class="hljs">`
- Left side returns the mongo/order payload
- Payload includes:
  - order id
  - order type
  - target entity `1700426781`
  - final state `FINISHED`
  - result code `GPON_000`
