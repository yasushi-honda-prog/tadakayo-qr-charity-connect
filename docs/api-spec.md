# API仕様（内部）

本ドキュメントは、**自社側のAPI仕様**を定義する。PayPay/楽天ペイの公式仕様は別途確認し、アダプタ層で差分吸収する。

## スコープ
- 対象: 寄付フローの開始、決済遷移、Webhook受信
- 目的: エンジニアが実装に着手できる最小仕様を明文化
- 注意: プロバイダ固有の必須項目は「要確認」として保留

## エンドポイント一覧

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/api/donations/checkout` | 寄付セッション作成・決済画面URLを返す |
| GET | `/api/donations/{donationId}` | 寄付状態の取得（フロント表示用） |
| POST | `/api/webhooks/paypay` | PayPayのWebhook受信 |
| POST | `/api/webhooks/rakuten` | 楽天ペイのWebhook受信 |

## リクエスト/レスポンス

### POST /api/donations/checkout

**Request (JSON)**
```json
{
  "amount": 1000,
  "currency": "JPY",
  "source": "flyer_a",
  "provider": "paypay",
  "returnUrl": "https://example.org/thanks",
  "cancelUrl": "https://example.org/cancel",
  "idempotencyKey": "uuid-v4"
}
```

**Response (JSON)**
```json
{
  "donationId": "don_123",
  "provider": "paypay",
  "redirectUrl": "https://paypay.ne.jp/...",
  "expiresAt": "2026-01-11T12:00:00Z",
  "status": "pending"
}
```

**Validation**
- `amount`: 最小/最大金額はプロバイダ規約で確定
- `source`: 既知のQRソースであること
- `provider`: `paypay` / `rakuten`
- `idempotencyKey`: 24時間以上の再利用禁止

### GET /api/donations/{donationId}

**Response (JSON)**
```json
{
  "donationId": "don_123",
  "status": "completed",
  "amount": 1000,
  "currency": "JPY",
  "provider": "paypay",
  "source": "flyer_a",
  "completedAt": "2026-01-11T12:05:00Z"
}
```

## Webhook仕様（共通方針）

### 署名検証
- 必須: HMAC署名または公開鍵署名を検証
- 失敗時は `401` を返却
- 署名検証の入力文字列・ヘッダはプロバイダ仕様で確定

### イベント処理
- 既処理判定: `providerEventId` + `provider` の組み合わせで重複排除
- 状態遷移: `pending` -> `completed` / `failed` / `refunded` / `expired`

### Webhookレスポンス
- 正常処理: `200 OK`
- 署名不一致: `401 Unauthorized`
- 不正ペイロード: `400 Bad Request`
- 一時障害: `500`（再送に備える）

## 状態遷移

```
pending -> completed
pending -> failed
pending -> expired
completed -> refunded
```

## エラーコード（内部）

| コード | 例 | 説明 |
|--------|----|------|
| INVALID_ARGUMENT | amount | 入力検証エラー |
| PROVIDER_UNAVAILABLE | paypay | 決済プロバイダ障害 |
| SIGNATURE_INVALID | webhook | 署名検証失敗 |
| DUPLICATE_EVENT | webhook | 既処理イベント |

## アダプタ設計（プロバイダ差分吸収）

**共通インターフェース（案）**
- `createCheckoutSession(input) -> { redirectUrl, providerOrderId }`
- `verifyWebhook(headers, body) -> { valid, event }`
- `normalizeEvent(event) -> { status, providerEventId, providerOrderId }`

**要確認事項（プロバイダ仕様反映後に確定）**
- 決済作成APIの必須フィールド
- Webhookの署名方式とヘッダ名
- 決済状態一覧と遷移規則
- 返金イベントの有無と仕様
