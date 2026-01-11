# AI駆動開発ガイド

本プロジェクトはAI支援を前提に、設計・実装・検証を高速化します。決済系の安全性とコンプライアンスが最重要のため、AIの出力は必ず人が最終レビューします。

## 参照すべき一次情報
- 仕様の源泉: `docs/architecture.md`, `docs/tech-stack.md`, `docs/api-spec.md`, `docs/data-model.md`, `docs/adr/`
- 調査結果: `docs/research/2026-01-11-qr-payment-research.md`
- 運用要件: `docs/operations.md`, `docs/monitoring.md`, `docs/testing.md`

## AIに渡すべき最小コンテキスト
- 目的とスコープ（何を作る/触らない）
- 決済プロバイダ（PayPay for Developers / 楽天ペイ）
- インフラ前提（Cloud Run / Firestore / Secret Manager / Cloud NAT）
- 受け入れ条件（例: 署名検証、idempotency、ログ規約）

## AIへの依頼テンプレート
```
目的: [何を達成したいか]
対象: [変更するファイル/コンポーネント]
前提: [参照ドキュメント、APIの前提]
制約: [セキュリティ/運用/規約]
受け入れ条件: [完了の定義]
テスト: [実施する確認]
```

## 変更時の必須ルール
- 設計判断はADRに記録（新規 or 既存更新）
- 仕様変更は docs/ に同期
- 決済フローは「失敗パス」まで確認する

## Definition of Done
- 決済セッション作成 + Webhook受信が通る
- 署名検証が実装され、失敗パスのテストがある
- 既処理判定（idempotency）が実装されている
- 依存関係と環境変数が `docs/` に反映されている
- 監視とアラートが `docs/operations.md` に反映されている

## セキュリティと秘匿情報
- シークレットは Secret Manager を使用
- APIキーや署名鍵をログに出力しない
- PII（氏名・メール等）はマスキング

## AIレビューの観点
- 決済の失敗パス/再送に対する堅牢性
- 署名検証の抜け漏れ
- 決済プロバイダ差分の吸収（PayPay/RakutenのAPI差異）
- 監視・アラートの不足
