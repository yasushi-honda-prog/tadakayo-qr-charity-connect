# QR決済寄付調査レポート

**調査日**: 2026年1月11日

## 調査目的

QRコードを使ったPayPay/楽天ペイでの寄付集めの実現方法を調査。

## 調査結果サマリー

| 決済サービス | 寄付対応 | 導入方法 |
|-------------|---------|---------|
| PayPay | ✅ 可能 | つながる募金 or コングラント or 直接契約 |
| 楽天ペイ | ❌ 非対応 | NPO向け寄付導入の情報なし |

## 詳細調査結果

### PayPay

#### PayPay for Developers（当初想定）
- **結論: 寄付目的での利用は規約違反**
- 公式FAQ: 「商取引ではない寄付や募金、投げ銭など一部NG商材」
- QRコードのSNS・Web掲載も規約違反（店舗加盟店の場合）
- URL: https://paypay.ne.jp/store-online/

#### PayPay法人ビジネスアカウント（寄付用）
- QRスキャン→即PayPay決済の体験
- 2025年3月〜街頭募金・施設内寄付に対応
- 厳重な審査（対面調査あり）
- 導入団体: 赤い羽根、国連WFP、東京大学など約20団体

#### つながる募金経由
- ソフトバンク運営の寄付プラットフォーム
- 2025年3月〜PayPay対応
- 手数料2.4%のみ、月額無料
- 720団体以上が利用
- URL: https://www.softbank.jp/corp/sustainability/esg/social/local-communities/tunagaru-bokin/npo/

#### コングラント経由
- 寄付決済・管理プラットフォーム
- PayPay対応（一部団体のみ）
- 月額4,000円〜 + 決済手数料4.4%
- 領収書自動発行、Salesforce連携
- URL: https://congrant.com/jp/

### 楽天ペイ

#### 楽天ペイ（オンライン決済）
- **結論: NPO向け寄付決済に対応していない**
- 公開情報では寄付導入に関する記載なし
- URL: https://checkout.rakuten.co.jp/biz/

#### 楽天クラッチ募金
- 楽天グループ運営の寄付プラットフォーム
- NPOが自由に導入できるものではない
- 決済手段: 楽天ポイント、楽天カード、VISA/Mastercard、楽天銀行振込
- **楽天ペイは決済手段に含まれていない**
- URL: https://corp.rakuten.co.jp/donation/

### その他のQR決済

| サービス | 寄付対応 |
|---------|---------|
| d払い | ○ NTTドコモ公式募金で対応 |
| au PAY | △ auじぶん銀行経由は可能 |
| LINE Pay | ○ 災害時の期間限定対応 |

## コスト比較

### 年間総コスト（月間寄付10万円想定）

| 選択肢 | 初期費用 | 年間運用費 | 合計 |
|--------|---------|-----------|------|
| つながる募金 | 0〜5万円 | 28,800円 | 約3〜8万円 |
| コングラント | 8〜15万円 | 100,800円 | 約11〜22万円 |
| PayPay直接契約 | 0円 | 要確認 | 要確認 |

## 推奨案

### フェーズ1（今すぐ）
**つながる募金で開始**
- 初期コスト: 0〜5万円
- 月額: 寄付額の2.4%のみ
- 審査: 約1ヶ月

### フェーズ2（認定NPO取得後・寄付拡大時）
**コングラントへ移行を検討**
- 領収書自動発行
- 寄付者管理の効率化
- 年間寄付額50万円超えたら費用対効果◎

## 参考リンク

### PayPay関連
- [PayPay 寄付・お賽銭](https://paypay.ne.jp/guide/donation/)
- [PayPay よくある規約違反行為](https://paypay.ne.jp/help-merchant/b0518/)
- [PayPay、街頭募金や施設内寄付への対応開始](https://paymentnavi.com/paymentnews/158625.html)

### 楽天関連
- [楽天クラッチ募金](https://corp.rakuten.co.jp/donation/)
- [楽天ペイガイドライン](https://checkout.rakuten.co.jp/rule.html)

### 寄付プラットフォーム
- [つながる募金（NPO向け）](https://www.softbank.jp/corp/sustainability/esg/social/local-communities/tunagaru-bokin/npo/)
- [コングラント](https://congrant.com/jp/)
- [コングラント料金](https://congrant.com/jp/fee.html)

### 法的解説
- [なぜPayPayを使った寄付は制限されているのか - STORIA法律事務所](https://storialaw.jp/blog/7076)
