# タダカヨ QRチャリティ・コネクト

QRコードを起点としたスマートフォン支援決済システム。チラシ・名刺・イベント投影のQRコードをスキャンするだけで、簡単に支援ができる仕組みを提供します。

## 概要

本システムは、NPO法人タダカヨの活動を支援するための決済プラットフォームです。PayPay for Developers / 楽天ペイのAPI連携により、決済フローを自前で制御します。

### 重要：対価性のある取引（売上）

タダカヨの「支援」は、研修の提供やグッズの提供など**対価性のある取引**であり、経理上は「売上」として計上します。この位置づけにより、PayPay for Developers / 楽天ペイは**商取引用途**として適合します。

## 特徴

- **簡単な支援体験**: QRコードをスキャンするだけで支援画面へ
- **複数の決済手段**: PayPay、楽天ペイに対応
- **流入元トラッキング**: チラシ・名刺・イベントごとの効果測定が可能（GA4）
- **拡張性**: サーバーレス構成で機能追加しやすい

## アーキテクチャ

```
QRコード (チラシ/名刺/スライド)
    ↓ スキャン
既存HP / ランディングページ
    ↓ 支援金額選択
Cloud Run API
    ↓ 決済セッション作成
PayPay / 楽天ペイ
    ↓ Webhook
Firestore 記録
```

### 使用サービス

- **PayPay for Developers / 楽天ペイ**: 決済処理（API連携）
- **Cloud Run / Firestore / Secret Manager / Cloud NAT**: 決済API連携とデータ管理
- **既存HP**: 支援案内ページ
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

決済プロバイダへの申請・契約準備中です。詳細は[ロードマップ](docs/roadmap.md)を参照してください。

## ライセンス

MIT License

## 関連リンク

- [タダカヨ公式サイト](https://mmky310.info/)
- [PayPay for Developers](https://paypay.ne.jp/store-online/)
- [楽天ペイ（オンライン決済）](https://checkout.rakuten.co.jp/biz/)
