# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

タダカヨ QRチャリティ・コネクト - QRコードを起点としたスマホ支援決済システム。チラシ・名刺・イベント投影のQRコードから支援ページへ遷移し、PayPay/楽天ペイで決済を完了する。

- GitHub: `tadakayo-qr-charity-connect`
- 決済プラットフォーム: PayPay for Developers / 楽天ペイ（API連携）

### 重要：対価性のある取引（売上）

タダカヨの「支援」は、研修の提供やグッズの提供など**対価性のある取引**であり、経理上は「売上」として計上する。これは現在の出張タダスク後の支援金も同様の扱いである。

この位置づけにより、PayPay for Developers / 楽天ペイは**商取引用途**として適合する。

## アーキテクチャ

```
QRコード → 既存HP / ランディングページ → Cloud Run → PayPay/楽天ペイ決済
                    ↓
              GA4（流入元トラッキング）
```

### 主要コンポーネント
- **既存HP**: 支援導線ページ、金額選択の入口
- **Cloud Run**: 決済セッション作成、Webhook受信、リダイレクト
- **Firestore**: 支援履歴、決済ステータス保存
- **PayPay/楽天ペイ**: 決済API
- **Google Analytics 4**: 流入元（QR種類）のトラッキング

### 技術選択
- インフラ: **GCPサーバーレス**（Cloud Run / Firestore / Secret Manager / Cloud NAT）
- 決済: PayPay for Developers / 楽天ペイ API連携

## 決済導入の流れ

1. PayPay for Developers / 楽天ペイに商取引として申請・契約
2. 既存HPに支援導線を追加（金額選択ページ）
3. 決済API連携（セッション作成、Webhook受信、署名検証）
4. QRコード作成と流入元パラメータの付与

## 開発コマンド

```bash
# srcディレクトリで実行
cd src

# テスト実行
uv run pytest tests/ -v

# lint
uv run ruff check app/

# 型チェック
uv run mypy app/

# ローカル起動
uv run uvicorn app.main:app --reload --port 8000
```

## ドキュメント参照ガイド

| タスク | 参照先 |
|--------|--------|
| API仕様確認 | `docs/api-spec.md` |
| 進捗確認 | `docs/roadmap.md` |
| 設計判断の経緯 | `docs/adr/` |
| 環境変数・シークレット | `docs/env-secrets.md` |
| データモデル | `docs/data-model.md` |

## 開発ルール

### ドキュメント同期
- 重要な設計変更はADRを作成（`docs/adr/`）
- 仕様・運用・セキュリティの変更は該当ドキュメントを更新

## 参考リンク
- [PayPay for Developers](https://paypay.ne.jp/store-online/)
- [楽天ペイ（オンライン決済）](https://checkout.rakuten.co.jp/biz/)

## 過去の検討事項
以下は調査の結果、採用しないことになった選択肢：
- つながる募金（新規受付停止のため見送り）
- コングラント（将来的な移行候補）
