# ADR-004: 決済プロバイダ選定 - PayPay/Rakuten API連携

## Status
Accepted

## Context

タダカヨ QRチャリティ・コネクトでは、QRコードを起点としたPayPay/楽天ペイでの寄付決済を実現する。以前は「つながる募金」を採用していたが、**新規受付停止の報告**があり、導入が不確実となった。

2026-01-11時点の公開情報（`docs/research/2026-01-11-qr-payment-research.md`）では以下の点が確認されている：

1. **PayPay for Developers は商取引用途が中心**
   - 寄付/募金用途の適合性が不明瞭であり、事前の確認が必須
2. **楽天ペイは寄付用途の導入情報が乏しい**
   - NPO向けの明確な導入ガイドがないため、事前確認が必須

## Decision

**PayPay for Developers / 楽天ペイ API連携で設計を進める。**

- 規約適合性は契約前に必ず確認する
- 不適合が判明した場合は、他の決済手段へ切り替える

## Consequences

### メリット
- 寄付フローを自社で制御できる
- 複数決済（PayPay/楽天ペイ）を統一UIで提供できる
- 流入元トラッキングや寄付金額の調整が柔軟

### デメリット
- 開発・運用コストが増える（API連携・インフラ構築）
- 署名検証やidempotencyなどセキュリティ実装が必須
- 規約適合性に関する確認作業が必要

### アーキテクチャ変更

**Before:**
```
QRコード → 既存HP → つながる募金 → PayPay決済
```

**After:**
```
QRコード → 既存HP → Cloud Run → PayPay/楽天ペイ → Webhook → Firestore
```

## Risks & Mitigations

| リスク | 対応策 |
|--------|--------|
| 寄付用途が規約上NG | 事前確認、必要なら別手段へ切替 |
| Webhook偽装 | 署名検証 + IP制限 + 監視 |
| 決済の再送/重複 | idempotency設計 |
| 運用負荷増加 | 監視/アラートの自動化 |

## Alternatives

### 1. つながる募金
- 新規受付停止が報告されており、導入が不確実

### 2. PayPay法人ビジネスアカウント直接契約
- UXは最良だが審査が厳格（対面調査あり）

### 3. コングラント
- 領収書自動発行など運用は優れるが月額コストが高い

## References

- [PayPay for Developers](https://paypay.ne.jp/store-online/)
- [楽天ペイ（オンライン決済）](https://checkout.rakuten.co.jp/biz/)
- [PayPay 寄付・お賽銭](https://paypay.ne.jp/guide/donation/)
