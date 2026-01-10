# 運用上の注意点

## セキュリティ
- 決済完了通知の署名検証（Signature検証）を必ず実施
- APIキーや署名鍵はSecret Managerで管理し、コードに埋め込まない
- Webhook受信エンドポイントはIP制限とレート制限を検討

## 審査・手続き
- 実装開始と同時に、PayPay/楽天ペイの加盟店審査（特に「寄付」利用の申請）を並行して進める
- 審査条件や利用規約の変更を継続的に確認

## 監視・障害対応
- Webhook失敗の検知（Cloud Logging + アラート）を整備
- エラー率やレイテンシのSLOを定義し、定点観測を行う

## データ保全
- Firestoreのバックアップ戦略を用意
- 個人情報の取り扱いに関するルールを明文化

## 参考リンク
- PayPay for Developers: https://paypay.ne.jp/store-online/
- 楽天ペイ: https://checkout.rakuten.co.jp/biz/
