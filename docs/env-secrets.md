# 環境変数・シークレット一覧

本ドキュメントは、Cloud Runで使用する設定値とSecret Managerの一覧を定義する。

## 原則
- シークレットは Secret Manager を利用
- 直接コードに埋め込まない
- 実運用名はプロバイダ公式仕様に合わせて確定

## 環境変数（Config）

| 変数名 | 必須 | 説明 |
|-------|------|------|
| PROJECT_ID | Yes | GCPプロジェクトID |
| REGION | Yes | デプロイリージョン |
| BASE_URL | Yes | 公開URL（Webhook署名の検証に利用する場合あり） |
| DEFAULT_CURRENCY | Yes | 通貨（例: JPY） |
| PROVIDER_TIMEOUT_MS | Yes | 外部APIのタイムアウト | 
| LOG_LEVEL | Yes | ログレベル |

## シークレット（Secret Manager）

| シークレット名（仮） | 必須 | 説明 |
|----------------------|------|------|
| PAYPAY_API_KEY | Yes | PayPay APIキー（名称は要確認） |
| PAYPAY_API_SECRET | Yes | PayPay署名鍵（名称は要確認） |
| PAYPAY_MERCHANT_ID | No | 取得できる場合のみ利用 |
| RAKUTEN_API_KEY | Yes | 楽天ペイAPIキー（名称は要確認） |
| RAKUTEN_API_SECRET | Yes | 楽天ペイ署名鍵（名称は要確認） |

## 追加予定（要確認）
- Webhook署名検証用の公開鍵または証明書
- 返金API利用時の追加クレデンシャル
