# CabinetScan AI - Payment Gateways & Merchant Account Registry

**Son Güncelleme:** 24 Kasım 2026  
**Yönetici:** İbrahim Karakoç (`karakoc.i@gmail.com`)  
**GitHub:** [federal216/cabinetscan](https://github.com/federal216/cabinetscan.git)

---

## 1. Creem.io (Merchant of Record - Birincil Entegrasyon)
- **Portal:** [https://creem.io/](https://creem.io/)
- **Kullanıcı Hesabı:** `karakoc.i@gmail.com`
- **Mağaza Adı:** `CabinetScan A`
- **İkamet Ülkesi:** Turkey (Onaylı)
- **Ürün:** CabinetScan AI — Master Clinical Dossier ($99, One-time)
- **Product ID:** `prod_75U0KNi7IDlRffo4MBN9R1`
- **Canlı Ödeme Bağlantısı (Live Payment Link):** [https://www.creem.io/payment/prod_75U0KNi7IDlRffo4MBN9R1](https://www.creem.io/payment/prod_75U0KNi7IDlRffo4MBN9R1)
- **Desteklenen Ödeme Tipleri:** Apple Pay, Google Pay, Global Kredi Kartları (Visa, Mastercard, Amex), USDC / Kripto
- **Payout Yöntemi:** Wise, USDC veya Banka Havalesi
- **Satış Başına Net Kazanç:** ~$94.74 / $99
- **Entegrasyon Dosyaları:**
  - `api/creem/initialize.js` (Checkout oturumu başlatıcı)
  - `api/creem/webhook.js` (Ödeme onay webhook dinleyicisi)
  - `index.html` (Frontend 1-tık checkout butonu ve lisans doğrulama)

### Çevre Değişkenleri (.env)
```env
CREEM_PRODUCT_ID=prod_75U0KNi7IDlRffo4MBN9R1
CREEM_PAYMENT_LINK=https://www.creem.io/payment/prod_75U0KNi7IDlRffo4MBN9R1
CREEM_API_KEY=creem_live_... (veya creem_test_...)
CREEM_MODE=live
```

---

## 2. Whop (Alternatif / İkincil Ödeme Seçeneği)
- **Portal:** [https://whop.com/](https://whop.com/)
- **Ödeme Planı:** `plan_ikEY1bP1Pk7di` ($99 Master Dossier)
- **Checkout URL:** `https://whop.com/checkout/plan_ikEY1bP1Pk7di`
- **Lisans Doğrulama Ön Eki:** `WHOP-...`

---

## 3. Payout Banka Bilgileri (Payoneer Citibank US)
Creem veya Dodo payout alanlarına girilecek global hesap bilgileri:
- **Banka Adı:** Citibank, N.A.
- **Banka Adresi:** 111 Wall Street, New York, NY 10043, USA
- **Routing / ABA (EFT):** `031100209`
- **Hesap Numarası:** `70580640002590994`
- **Hesap Türü:** Checking (Vadesiz)
- **Lehdar:** İbrahim Karakoç
