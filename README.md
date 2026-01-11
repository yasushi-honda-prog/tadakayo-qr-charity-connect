# タダカヨ QRチャリティ・コネクト

QRコードを起点としたスマートフォン寄付システム。チラシ・名刺・イベント投影のQRコードをスキャンするだけで、簡単に寄付ができる仕組みを提供します。

## 概要

本システムは、NPO法人タダカヨの活動を支援するための寄付プラットフォームです。PayPay for Developers / 楽天ペイのAPI連携により、寄付フローを自前で制御します。

## 特徴

- **簡単な寄付体験**: QRコードをスキャンするだけで寄付画面へ
- **複数の決済手段**: PayPay、楽天ペイに対応
- **流入元トラッキング**: チラシ・名刺・イベントごとの効果測定が可能（GA4）
- **拡張性**: サーバーレス構成で機能追加しやすい

## アーキテクチャ

```
QRコード (チラシ/名刺/スライド)
    ↓ スキャン
既存HP / ランディングページ
    ↓ 寄付金額選択
Cloud Run API
    ↓ 決済セッション作成
PayPay / 楽天ペイ
    ↓ Webhook
Firestore 記録
```

### 使用サービス

- **PayPay for Developers / 楽天ペイ**: 寄付決済処理（API連携）
- **Cloud Run / Firestore / Secret Manager / Cloud NAT**: 決済API連携とデータ管理
- **既存HP**: 寄付案内ページ
- **Google Analytics 4**: 流入元トラッキング

## ドキュメント

- [アーキテクチャ概要](docs/architecture.md)
- [技術スタック詳細](docs/tech-stack.md)
- [API仕様（内部）](docs/api-spec.md)
- [データモデル](docs/data-model.md)
- [環境変数・シークレット一覧](docs/env-secrets.md)
- [監視・アラート](docs/monitoring.md)
- [テスト計画](docs/testing.md)
- [開発ロードマップ](docs/roadmap.md)
- [運用ガイド](docs/operations.md)
- [AI駆動開発ガイド](docs/ai-development.md)
- [ADR一覧](docs/adr/)
- [調査レポート](docs/research/)

## 開発状況

決済プロバイダの適合性確認と契約準備中です。詳細は[ロードマップ](docs/roadmap.md)を参照してください。

## 重要な制約事項

調査の結果、以下が判明しました（詳細は[ADR-004](docs/adr/ADR-004-payment-provider-selection.md)参照）：

- **PayPay for Developers**: 寄付用途の適合性は要確認
- **楽天ペイ**: 寄付用途の導入可否は要確認
- **つながる募金**: 新規受付停止が報告されているため導入を見送り

## ライセンス

MIT License

## 関連リンク

- [タダカヨ公式サイト](https://tadakayo.org/)
- [PayPay for Developers](https://paypay.ne.jp/store-online/)
- [楽天ペイ（オンライン決済）](https://checkout.rakuten.co.jp/biz/)
- [PayPay 寄付・お賽銭](https://paypay.ne.jp/guide/donation/)
