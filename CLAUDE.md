# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

タダカヨ QRチャリティ・コネクト - QRコードを起点としたスマホ寄付システム。チラシ・名刺・イベント投影のQRコードから寄付ページへ遷移し、PayPay等で寄付を完了する。

- GitHub: `tadakayo-qr-charity-connect`
- 寄付プラットフォーム: ソフトバンク「つながる募金」

## アーキテクチャ

```
QRコード → 既存HP / ランディングページ → つながる募金 → PayPay決済
                    ↓
              GA4（流入元トラッキング）
```

### 主要コンポーネント
- **既存HP**: 寄付導線ページ、つながる募金へのリンク
- **つながる募金**: 寄付決済処理（PayPay、クレカ、携帯料金合算）
- **Google Analytics 4**: 流入元（QR種類）のトラッキング

### 技術選択
- インフラ: **不要**（既存HPを活用、GCPインフラは使用しない）
- 決済: つながる募金経由（API開発不要）

## 重要な制約事項

### PayPay/楽天ペイについて
- **PayPay for Developers**: 寄付目的での利用は**規約違反**（商取引専用）
- **楽天ペイ**: NPO向け寄付決済に**対応していない**
- **つながる募金**: PayPay寄付に対応（2025年3月〜）

### 寄付決済の導入方法
1. つながる募金への申し込み（審査約1ヶ月）
2. 既存HPに寄付リンク追加
3. チラシ用QRコード作成

## 開発ルール

### ドキュメント同期
- 重要な設計変更はADRを作成（`docs/adr/`）
- 仕様・運用・セキュリティの変更は該当ドキュメントを更新

## 参考リンク
- [つながる募金（NPO向け）](https://www.softbank.jp/corp/sustainability/esg/social/local-communities/tunagaru-bokin/npo/)
- [PayPay 寄付・お賽銭](https://paypay.ne.jp/guide/donation/)
- [コングラント（将来の移行先候補）](https://congrant.com/jp/)

## 過去の検討事項
以下は調査の結果、採用しないことになった選択肢：
- PayPay for Developers（寄付NG）: ~~https://paypay.ne.jp/store-online/~~
- 楽天ペイ オンライン決済（寄付非対応）: ~~https://checkout.rakuten.co.jp/biz/~~
- GCPインフラ（Cloud Run, Firestore等）: 不要と判断
