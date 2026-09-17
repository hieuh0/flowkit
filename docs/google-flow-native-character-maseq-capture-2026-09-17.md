# Google Flow native Character `maseQ` capture

Captured from native Character creation on frontend build `boq_labs-ai-sandbox-frontend_20260915.10_p0`.

Sanitized fixture: no cookies, `at` tokens, reCAPTCHA values, account/session/client identifiers, project IDs, Character IDs, signed URLs, or image contents.

## RPC

```text
maseQ
```

## Decoded inner request payload

```json
[
  [
    null,
    22,
    null,
    null,
    null,
    "<PROJECT_UUID>",
    null,
    null,
    null,
    null,
    ["<CAPTCHA_TOKEN>", 1]
  ],
  "<IMAGE_BASE64>",
  "image/png",
  1,
  null,
  null,
  null,
  null,
  "ui.png",
  [null, null, ["<CHARACTER_UUID>", [0]]],
  "<CLIENT_UUID_1>",
  "<CLIENT_UUID_2>"
]
```

Observed serialized request body length: `2162967` bytes.

`payload[0][5]` is the project UUID. `payload[0][10][0]` is the CAPTCHA token. `payload[1]` is portrait image base64. `payload[9][2][0]` is the native Character UUID. `payload[10]` and `payload[11]` are fresh client UUIDs.

The matching successful response was captured from one fresh bind on a newly created Character in a disposable Google Flow project. UUIDs and signed values are sanitized below.

## Decoded successful response payload

```json
[
  [
    "<UPLOADED_MEDIA_UUID>",
    "<PROJECT_UUID>",
    "<WORKFLOW_UUID>",
    "CAE",
    null,
    [
      [[1789618518, 417850000], null, null, null, null, null,
       [null, null, null, null, 1], null, null, 1, null, null, null, 406216],
      [null, [null, null, null, null, 0], [1536, 1024]]
    ]
  ],
  [
    "<WORKFLOW_UUID>",
    null,
    null,
    ["ui.png", [1789618518, 417850000], null, null, "<UPLOADED_MEDIA_UUID>"],
    "<PROJECT_UUID>",
    "<CHARACTER_UUID>"
  ]
]
```

Identifier roles are established by equality with the request and create records:

- `0[0]` and `1[3][4]` are the uploaded portrait media UUID.
- `0[1]` and `1[4]` are the project UUID.
- `0[2]` and `1[0]` are the workflow UUID.
- `1[5]` is the native Character UUID.
