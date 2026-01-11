# データモデル（Firestore）

本ドキュメントはFirestoreのコレクション設計と制約を定義する。

## コレクション一覧

- `donations` : 寄付の主データ
- `payment_events` : Webhookイベントの監査ログ
- `qr_sources` : QRコード流入元のマスタ

## donations

| フィールド | 型 | 必須 | 説明 |
|-----------|----|------|------|
| id | string | Yes | FirestoreのドキュメントID |
| amount | number | Yes | 寄付金額（最小/最大は規約で確定） |
| currency | string | Yes | 通貨（固定で JPY） |
| provider | string | Yes | `paypay` / `rakuten` |
| status | string | Yes | `pending`/`completed`/`failed`/`refunded`/`expired` |
| source | string | Yes | 流入元（qr_sources.id） |
| providerOrderId | string | Yes | 決済プロバイダ側の注文ID |
| providerCustomerId | string | No | プロバイダが返す顧客ID（任意） |
| idempotencyKey | string | Yes | セッション作成時の冪等キー |
| createdAt | timestamp | Yes | 作成日時 |
| updatedAt | timestamp | Yes | 更新日時 |
| completedAt | timestamp | No | 決済完了日時 |

**インデックス候補**
- `provider + providerOrderId`（一意性担保のため）
- `status + createdAt`
- `source + createdAt`

## payment_events

| フィールド | 型 | 必須 | 説明 |
|-----------|----|------|------|
| id | string | Yes | FirestoreのドキュメントID |
| provider | string | Yes | `paypay` / `rakuten` |
| providerEventId | string | Yes | プロバイダが付与するイベントID |
| providerOrderId | string | Yes | 注文ID |
| status | string | Yes | 正規化後のステータス |
| receivedAt | timestamp | Yes | 受信日時 |
| rawPayload | map | Yes | 受信ペイロード（PIIはマスキング） |
| signatureValid | boolean | Yes | 署名検証結果 |

**インデックス候補**
- `provider + providerEventId`（重複排除）
- `providerOrderId + receivedAt`

## qr_sources

| フィールド | 型 | 必須 | 説明 |
|-----------|----|------|------|
| id | string | Yes | 例: `flyer_a` |
| name | string | Yes | 表示名 |
| type | string | Yes | `flyer`/`card`/`event` |
| active | boolean | Yes | 有効フラグ |
| createdAt | timestamp | Yes | 作成日時 |
| description | string | No | 説明 |

## 制約・ルール

- `providerOrderId` は `donations` 内で一意
- `providerEventId` は `payment_events` 内で一意
- `status` の更新はWebhookによってのみ行う
- `rawPayload` はPIIをマスキングして保存する
