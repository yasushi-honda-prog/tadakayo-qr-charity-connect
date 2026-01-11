# タダカヨ QRチャリティ・コネクト

QRコードを起点としたスマートフォン寄付システム。チラシ・名刺・イベント投影のQRコードをスキャンするだけで、簡単に寄付ができる仕組みを提供します。

## 概要

本システムは、NPO法人タダカヨの活動を支援するための寄付プラットフォームです。ソフトバンク「つながる募金」を活用し、PayPayやクレジットカードでスムーズに寄付を完了できます。

## 特徴

- **簡単な寄付体験**: QRコードをスキャンするだけで寄付画面へ
- **複数の決済手段**: PayPay、クレジットカード、携帯料金合算に対応
- **流入元トラッキング**: チラシ・名刺・イベントごとの効果測定が可能（GA4）
- **低コスト運用**: 月額無料、手数料2.4%のみ

## アーキテクチャ

```
QRコード (チラシ/名刺/スライド)
    ↓ スキャン
既存HP / ランディングページ
    ↓ リンク
つながる募金（寄付ページ）
    ↓ 決済
PayPay / クレカ / 携帯料金合算
```

### 使用サービス

- **つながる募金**: 寄付決済処理（ソフトバンク運営）
- **既存HP**: 寄付案内ページ
- **Google Analytics 4**: 流入元トラッキング

## ドキュメント

- [アーキテクチャ概要](docs/architecture.md)
- [技術スタック詳細](docs/tech-stack.md)
- [開発ロードマップ](docs/roadmap.md)
- [運用ガイド](docs/operations.md)
- [AI駆動開発ガイド](docs/ai-development.md)
- [ADR一覧](docs/adr/)
- [調査レポート](docs/research/)

## 開発状況

つながる募金への申し込み準備中です。詳細は[ロードマップ](docs/roadmap.md)を参照してください。

## 重要な制約事項

調査の結果、以下が判明しました（詳細は[ADR-004](docs/adr/ADR-004-payment-provider-selection.md)参照）：

- **PayPay for Developers**: 寄付目的での利用は規約違反
- **楽天ペイ**: NPO向け寄付決済に非対応
- **つながる募金**: PayPay寄付に対応（2025年3月〜）

## ライセンス

MIT License

## 関連リンク

- [タダカヨ公式サイト](https://tadakayo.org/)
- [つながる募金（NPO向け）](https://www.softbank.jp/corp/sustainability/esg/social/local-communities/tunagaru-bokin/npo/)
- [PayPay 寄付・お賽銭](https://paypay.ne.jp/guide/donation/)
