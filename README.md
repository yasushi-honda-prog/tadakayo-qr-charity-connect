# タダカヨ QRチャリティ・コネクト

QRコードを起点としたスマートフォン寄付システム。チラシ・名刺・イベント投影のQRコードをスキャンするだけで、簡単に寄付ができる仕組みを提供します。

## 概要

本システムは、NPO法人タダカヨの活動を支援するための寄付プラットフォームです。紙媒体やイベント投影に印刷されたQRコードから、PayPayや楽天ペイなどの決済サービスを通じてスムーズに寄付を完了できます。

## 特徴

- **簡単な寄付体験**: QRコードをスキャンするだけで寄付画面へ
- **複数の決済手段**: PayPay、楽天ペイに対応（順次拡大予定）
- **流入元トラッキング**: チラシ・名刺・イベントごとの効果測定が可能
- **低コスト運用**: GCPサーバーレス構成による従量課金

## アーキテクチャ

```
QRコード (チラシ/名刺/スライド)
    ↓ スキャン
Cloud Run (Backend API)
    ↓ 決済リクエスト
PayPay / 楽天ペイ API
    ↓ Webhook通知
Cloud Firestore (寄付記録)
```

### 使用技術

- **Cloud Run**: APIエンドポイント、決済遷移、Webhook受信
- **Cloud Firestore**: 寄付履歴・決済ステータス・流入元の保存
- **Secret Manager**: APIキー・署名鍵の安全な管理
- **Cloud NAT**: 決済プロバイダ向け固定IP
- **Terraform**: インフラのコード管理

## ドキュメント

- [アーキテクチャ概要](docs/architecture.md)
- [技術スタック詳細](docs/tech-stack.md)
- [開発ロードマップ](docs/roadmap.md)
- [運用ガイド](docs/operations.md)
- [AI駆動開発ガイド](docs/ai-development.md)
- [ADR一覧](docs/adr/)

## 開発状況

現在、第1段階（MVP）の構築中です。詳細は[ロードマップ](docs/roadmap.md)を参照してください。

## ライセンス

MIT License

## 関連リンク

- [タダカヨ公式サイト](https://tadakayo.org/)
- [PayPay for Developers](https://paypay.ne.jp/store-online/)
- [楽天ペイ](https://checkout.rakuten.co.jp/biz/)
