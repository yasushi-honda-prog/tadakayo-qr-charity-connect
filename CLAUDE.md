# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

タダカヨ QRチャリティ・コネクト - QRコードを起点としたスマホ寄付システム。チラシ・名刺・イベント投影のQRコードから寄付ページへ遷移し、PayPay/楽天ペイで寄付を完了する。

- GitHub: `tadakayo-qr-charity-connect`
- 寄付プラットフォーム: PayPay for Developers / 楽天ペイ（API連携）

## アーキテクチャ

```
QRコード → 既存HP / ランディングページ → Cloud Run → PayPay/楽天ペイ決済
                    ↓
              GA4（流入元トラッキング）
```

### 主要コンポーネント
- **既存HP**: 寄付導線ページ、寄付金額選択の入口
- **Cloud Run**: 決済セッション作成、Webhook受信、リダイレクト
- **Firestore**: 寄付履歴、決済ステータス保存
- **PayPay/楽天ペイ**: 決済API
- **Google Analytics 4**: 流入元（QR種類）のトラッキング

### 技術選択
- インフラ: **GCPサーバーレス**（Cloud Run / Firestore / Secret Manager / Cloud NAT）
- 決済: PayPay for Developers / 楽天ペイ API連携

## 重要な制約事項

### PayPay/楽天ペイについて
- 2026-01-11時点の公開情報では、寄付用途の適合性がグレー/不明瞭な点があるため、**事前に規約確認と窓口確認が必須**
- **PayPay for Developers**: 商取引向けの記載が中心。寄付/募金用途の適用可否を確認する
- **楽天ペイ**: NPO向け寄付の明確な導入記載が乏しいため、利用可否を確認する

### 寄付決済の導入方法
1. PayPay for Developers / 楽天ペイの事前審査・契約
2. 既存HPに寄付導線を追加（寄付金額選択ページ）
3. 決済API連携（セッション作成、Webhook受信、署名検証）
4. QRコード作成と流入元パラメータの付与

## 開発ルール

### ドキュメント同期
- 重要な設計変更はADRを作成（`docs/adr/`）
- 仕様・運用・セキュリティの変更は該当ドキュメントを更新

## 参考リンク
- [PayPay for Developers](https://paypay.ne.jp/store-online/)
- [楽天ペイ（オンライン決済）](https://checkout.rakuten.co.jp/biz/)
- [PayPay 寄付・お賽銭](https://paypay.ne.jp/guide/donation/)

## 過去の検討事項
以下は調査の結果、採用しないことになった選択肢：
- つながる募金（新規受付停止のため見送り）
- コングラント（将来的な移行候補）
