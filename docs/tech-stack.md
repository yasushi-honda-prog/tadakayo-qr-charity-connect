# 詳細技術スタック

## アプリケーション
- Frontend/Backend: Node.js (Express) または Python (FastAPI)
  - Cloud Run上で稼働し、APIと寄付開始ページを提供
  - 実装フェーズで比較検討し、ADRで決定

## データストア
- Cloud Firestore (Native Mode)
  - 寄付履歴、決済ステータス、流入元、通知ログを保持

## セキュリティ
- Secret Manager
  - 決済APIキー、Webhook署名鍵、管理用トークンを保管

## ネットワーク
- Cloud NAT / Cloud Router
  - 決済プロバイダ向け固定IPを確保
  - 送信元IPをホワイトリストに登録して審査対応

## インフラ/運用
- Terraform
  - GCPリソースのIaC管理
- GitHub
  - 仕様・設計・実装を一元管理
- Claude Code
  - 仕様整理、コード補助、ドキュメント更新の支援

## 監視・可観測性（検討）
- Cloud Logging / Cloud Monitoring
  - APIエラー、Webhook失敗のアラート通知
- Error Reporting
  - 例外発生時の集約
