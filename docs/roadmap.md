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
- [ ] GitHub連携の設定（Workload Identity等）
- [ ] Cloud Run / Firestore / Secret Manager 構築
- [ ] Cloud NAT構築（固定IPの確保）
- [ ] 監視・ログ基盤の最低限セットアップ

## 第3段階: MVP実装

- [ ] 支援金額選択ページの作成
- [ ] PayPay決済セッション作成API
- [ ] PayPay Webhook受信 + 署名検証
- [ ] Firestoreへの支援記録保存
- [ ] サンクスページ表示

## 第4段階: 複数決済対応

- [ ] 楽天ペイ決済セッション作成API
- [ ] 楽天ペイ Webhook受信 + 署名検証
- [ ] 決済プロバイダ差分の抽象化

## 第5段階: 運用・分析強化

- [ ] GA4の流入元トラッキング
- [ ] 決済成功率/失敗率の可視化
- [ ] 支援者問い合わせフローの整備

## 継続的改善

- [ ] 支援者へのお礼・報告の仕組み構築
- [ ] 支援キャンペーンの企画・実施
- [ ] 認定NPO取得後の寄付金控除案内整備（対価性のない寄付を受ける場合）
