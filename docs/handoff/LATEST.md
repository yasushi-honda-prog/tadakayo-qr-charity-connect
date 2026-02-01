# ハンドオフメモ

**最終更新**: 2026-02-01

## 現在のフェーズ

第3段階: MVP実装 → **Sandbox環境でのテスト中**

## 直近の変更（2026-02-01）

| 変更 | 概要 |
|------|------|
| Sandbox環境説明追加 | thanks.html, cancel.htmlにテスター向けSandbox制限の説明を追加 |
| GitHub Pages更新 | docs/index.htmlにSandbox環境の既知の制限を追記 |
| 印刷用ページ簡素化 | print.html, print-donate.htmlから不要なセクションを削除 |
| ブラウザバック修正 | donate.htmlにpageshowイベントでローディング非表示を追加 |
| 自由金額印刷ボタン修正 | 入力金額に対応したQRコード生成に修正 |

## MVP実装状況

| 機能 | 状態 | 備考 |
|------|------|------|
| 管理画面 (`/donate`) | ✅ | 金額選択、QR生成、決済実行 |
| 印刷用QR (`/print/{amount}`) | ✅ | 固定金額QR発行 |
| 決済ページ (`/pay/{amount}`) | ✅ | PayPay決済実行 |
| サンクスページ | ✅ | Sandbox説明付き |
| キャンセルページ | ✅ | Sandbox説明付き |
| PayPay決済API | ✅ | Sandbox接続済み |
| 楽天ペイ | 🔜 | モック版完了、本番接続待ち |

## デモ環境

| 環境 | URL |
|------|-----|
| Cloud Run Sandbox | https://qr-payment-api-sandbox-yggvw3tpqa-an.a.run.app |
| GitHub Pages | https://yasushi-honda-prog.github.io/tadakayo-qr-charity-connect/ |

## 既知の制限（Sandbox環境）

- PayPayアプリで決済完了後、ブラウザへのリダイレクトが正常に動作しないことがある
- 決済自体は成功しているが、thanks.htmlではなくcancel.htmlに遷移する場合がある
- **本番環境では正常動作する見込み**

## 次のアクション候補

1. テスターからのフィードバック収集
2. 楽天ペイの実装（Phase 2）
3. 本番環境へのデプロイ準備
4. PayPay for Developers 本番申請

## デプロイ済みインフラ

- Cloud Run: Sandbox環境稼働中
- Firestore: InMemoryモード（Sandbox）
- Cloud NAT: 固定IP 34.84.72.66
- GitHub Actions: CI/CD設定済み
