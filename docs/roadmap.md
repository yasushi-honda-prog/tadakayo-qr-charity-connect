# 段階的開発ロードマップ

## 第1段階: 契約・準備

- [x] 申請要件の整理（[docs/payment-provider-application.md](payment-provider-application.md)）
- [ ] PayPay for Developers に商取引として申請
  - 研修・グッズ等のサービス/商品提供として申請
  - 必要書類の準備（法人情報、銀行口座等）
- [ ] 楽天ペイ（オンライン決済）に商取引として申請
- [ ] 審査・契約フローを完了
- [ ] Webhook受信先やIP制限の要件整理

## 第2段階: インフラ整備

- [x] GCPプロジェクト作成（tadakayo-qr-connect）
- [x] GitHub連携の設定（Workload Identity Federation）
- [x] Cloud Run / Firestore / Secret Manager 構築
- [x] Cloud NAT構築（固定IP: 34.84.72.66）
- [x] Artifact Registry（最新2バージョン保持ポリシー）
- [ ] 監視・ログ基盤の最低限セットアップ

**構築済みリソース:**
- Cloud Run: https://qr-payment-api-sandbox-yggvw3tpqa-an.a.run.app
- Terraform: `infrastructure/environments/sandbox/`
- CI/CD: `.github/workflows/ci.yml`, `deploy-sandbox.yml`

## 第3段階: MVP実装

- [x] 支援金額選択ページの作成（`/donate`）
- [x] PayPay決済セッション作成API（モック版完了、本番接続は審査後）
- [x] PayPay Webhook受信 + 署名検証（モック版完了）
- [x] Firestoreへの支援記録保存（InMemory + Firestore両対応）
- [x] サンクスページ表示（`/thanks`）
- [x] キャンセルページ表示（`/cancel`）
- [x] 固定金額QRコード機能（`/qr/{amount}`）
  - QRスキャン → PayPay決済ページ直接遷移
  - チラシ・名刺用の印刷用QRコード発行

**実装済みコンポーネント:**
- `src/app/adapters/` - 決済プロバイダアダプタ（PayPay/楽天ペイ）
- `src/app/services/payment.py` - 決済サービス
- `src/app/api/donations.py` - APIエンドポイント
- `src/app/static/` - 静的ページ（donate.html, thanks.html, cancel.html, qr-payment.html）
- `src/tests/unit/` - ユニットテスト30件

## 第4段階: 複数決済対応

- [x] 楽天ペイ決済セッション作成API（モック版完了）
- [x] 楽天ペイ Webhook受信 + 署名検証（モック版完了）
- [x] 決済プロバイダ差分の抽象化（PaymentProviderAdapter ABC）

## 第5段階: 運用・分析強化

- [ ] GA4の流入元トラッキング
- [ ] 決済成功率/失敗率の可視化
- [ ] 支援者問い合わせフローの整備

## 継続的改善

- [ ] 支援者へのお礼・報告の仕組み構築
- [ ] 支援キャンペーンの企画・実施
- [ ] 認定NPO取得後の寄付金控除案内整備（対価性のない寄付を受ける場合）
