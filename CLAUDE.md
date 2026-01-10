# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

タダカヨ QRチャリティ・コネクト - QRコードを起点としたスマホ寄付システム。チラシ・名刺・イベント投影のQRコードから決済プロバイダ（PayPay/楽天ペイ）へ遷移し、寄付を完了する。

- GitHub: `tadakayo-qr-charity-connect`
- GCP Project: `tadakayo-qr-connect`

## アーキテクチャ

```
QRコード → Cloud Run (Backend) → 決済API (PayPay/楽天ペイ)
                ↓                      ↓
           Firestore ←────── Webhook通知
                ↑
          Secret Manager (APIキー/署名鍵)
```

### 主要コンポーネント
- **Cloud Run**: APIエンドポイント、決済遷移、Webhook受信
- **Firestore (Native Mode)**: 寄付履歴・決済ステータス・流入元（QR種類）を保存
- **Secret Manager**: 決済APIキー、Webhook署名鍵
- **Cloud NAT**: 決済プロバイダ向け固定IP（ホワイトリスト登録用）

### 技術選択（予定）
- アプリケーション: Node.js (Express) または Python (FastAPI) - 実装フェーズで決定
- インフラ: Terraform (IaC)

## 開発ルール

### Webhook/決済関連
- **署名検証は必須**: 決済完了通知のSignature検証を必ず実装
- **シークレット管理**: APIキー・署名鍵はSecret Managerで管理、コードに埋め込まない
- **ログ出力禁止項目**: APIキー、署名鍵、PII（個人情報）をログに出力しない

### ドキュメント同期
- 重要な設計変更はADRを作成（`docs/adr/`）
- 仕様・運用・セキュリティの変更は該当ドキュメントを更新
- 依存関係と環境変数は`docs/`に反映

## 参考リンク
- [PayPay for Developers](https://paypay.ne.jp/store-online/)
- [楽天ペイ](https://checkout.rakuten.co.jp/biz/)
