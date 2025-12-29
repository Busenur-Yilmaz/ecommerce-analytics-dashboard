#  E-Commerce Analytics Dashboard
https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/Pandas-2.1+-green.svg
https://img.shields.io/badge/Power%20BI-Desktop-yellow.svg
https://img.shields.io/badge/SQLite-3-orange.svg

## Proje Hakkında
Bu proje, Brazilian E-Commerce Public Dataset (Olist) kullanılarak Python, SQL ve Power BI ile end-to-end veri analizi ve görselleştirme çalışmasıdır. Proje, veri mühendisliği, veri bilimi ve iş zekası (BI) süreçlerinin tamamını kapsar.

## Proje Amaçları

 Ham veriden anlamlı içgörülere ulaşmak
 SQL veritabanı tasarımı ve optimizasyonu
 İnteraktif ve kullanıcı dostu dashboard oluşturma
 Veri kalitesi ve doğruluğu için best practice'leri uygulamak
 Teknik dokümantasyon ve versiyon kontrolü

##  Proje Yapısı

```
HAFTA7_Ecommerce_Dashboard/
├── data/
│   ├── raw/                  # Kaggle'dan indirilen ham CSV'ler
│   ├── processed/            # Temizlenmiş CSV'ler
│   └── database/             # SQLite veritabanı (ecommerce.db)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_data_merging.ipynb
├── scripts/
│   ├── 04_create_database.py
│   ├── 05_sql_analysis_queries.sql
│   └── 06_run_sql_analysis.py
├── powerbi/
│   └── ecommerce_dashboard.pbix
|   |__screenshoots
└── reports/
    └── sql_results/          # SQL sorgu sonuçları
```

---

##  Kurulum

### 1. Python Gereksinimleri

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### 2. Veri Setini İndirme

**Kaggle API:**
```bash
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw/ --unzip
```

**Manuel:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

### 3. SQLite ODBC Driver (Power BI için)

1. İndir: http://www.ch-werner.de/sqliteodbc/
2. `sqliteodbc_w64.exe` kur
3. ODBC DSN oluştur: `Ecommerce_SQLite`

---

##  Çalıştırma Adımları

### Python Pipeline:

```bash
# 1-3. Jupyter Notebooks
jupyter notebook notebooks/01_data_exploration.ipynb
jupyter notebook notebooks/02_data_cleaning.ipynb
jupyter notebook notebooks/03_data_merging.ipynb

# 4. SQLite DB oluştur
python scripts/04_create_database.py

# 5. SQL analizleri çalıştır
python scripts/06_run_sql_analysis.py
```

### Power BI:

1. Power BI Desktop aç
2. **Get Data** → **ODBC** → `Ecommerce_SQLite`
3. Tabloları **Import Mode** ile yükle
4. Model ve dashboard oluştur

---

##  Veri Seti

**Kaynak:** Brazilian E-Commerce (Olist) - Kaggle  
**Zaman:** 2016-2018  
**Coğrafya:** Brezilya

| Tablo | Satır | Açıklama |
|-------|-------|----------|
| orders | 96K | Sipariş bilgileri |
| customers | 99K | Müşteri bilgileri |
| order_items | 112K | Sipariş kalemleri |
| products | 33K | Ürün özellikleri |
| sellers | 3K | Satıcı bilgileri |
| payments | 104K | Ödeme bilgileri |
| reviews | 99K | Müşteri yorumları |
| geolocation | 19K | Coğrafi veriler |

---

##  Veri İşleme

### 1. Veri Keşfi
- İstatistiksel analiz
- Eksik değer kontrolü
- Veri kalitesi değerlendirmesi

### 2. Veri Temizleme
- Tarih formatları düzeltildi
- Negatif/hatalı değerler temizlendi
- Standartlaştırma yapıldı
- Yeni feature'lar oluşturuldu

### 3. SQLite Veritabanı
- 9 tablo yüklendi
- 15 index oluşturuldu
- Star schema tasarımı

---

##  Karşılaşılan Sorunlar ve Çözümler

###  Problem 1: CSV'de Negatif Değerler

**Sorun:**  
`final_merged_data.csv` dosyasında `total_payment_value` negatif değerler gösteriyordu:
- Power BI'da: `-5E+18` (bilimsel notasyon)
- KPI'lar tamamen yanlış hesaplanıyordu

**Kök Neden:**
- CSV'ye yazarken float overflow
- Veri tipi bilgisi kaybı
- Datetime kolonları sayısal değer olarak yorumlandı

** Çözüm: SQLite Veritabanı + İlişkisel Model**

CSV yerine SQLite kullanarak:
1. **Veri tipleri korundu** (float, datetime, varchar)
2. **Tablolar arası ilişkiler kuruldu:**
   ```
   orders → order_items (1:N)
   orders → customers (N:1)
   orders → payments (1:1)
   order_items → products (N:1)
   ```
3. **ODBC ile Power BI'a bağlandı**
4. **Doğru sonuçlar elde edildi:**
   - Total Revenue: $15.84M 
   - Avg Order Value: $164.23 

**Öğrenilen:**
-  CSV büyük veri setleri için güvenilir değil
-  İlişkisel veritabanları veri bütünlüğünü korur
-  Foreign key ilişkileri veri doğruluğunu artırır
---

###  Problem 2: Çifte Ciro Hatası

**Sorun:**  
Aynı `order_id` için birden fazla payment kaydı → KPI'lar şişiriliyordu

** Çözüm:**  
Power Query'de `payments` tablosunu `order_id` bazında tekilleştirdik:
```powerquery
= Table.Group(payments, {"order_id"}, 
    {{"total_payment_value", each List.Sum([payment_value])}}
)
```

**Sonuç:** 103K → 96K satır (order başına tek kayıt)

---

##  Power BI Dashboard

### Veri Bağlantısı
- **ODBC** üzerinden SQLite'a bağlandı
- **Import Mode** kullanıldı (DirectQuery değil)
- **5 ana tablo** yüklendi

### Model İlişkileri (Star Schema)

```
         customers
              ↓
           orders (Fact)
         ↙  ↓  ↘
order_items  payments  reviews
     ↓
  products
```

**İlişki Türleri:**
- `orders → order_items`: 1:N (Single Direction)
- `orders → customers`: N:1 (Single Direction)
- `orders → payments`: 1:1 (Single Direction)
- `order_items → products`: N:1 (Single Direction)

### Power Query Dönüşümleri
- Veri tipleri düzeltildi (datetime, decimal, currency)
- `payments` tekilleştirildi
- NULL değerler temizlendi

### DAX Measures

```dax
Total Revenue = SUM(payments[total_payment_value])

Total Orders = DISTINCTCOUNT(orders[order_id])

Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

Total Customers = DISTINCTCOUNT(customers[customer_unique_id])

Total Products = DISTINCTCOUNT(products[product_id])
```

### Dashboard Sayfaları

**1. Executive Summary**
- KPI kartları (Revenue, Orders, Avg Value, Customers, Products)
- Monthly Revenue Trend
- Delivery Performance
- Top 5 Categories

**2. Sales & Delivery Analysis**
- Quarterly/Yearly Revenue
- Orders by Month
- Top 10 Cities
- Top Sellers Table

**3. Customer Analysis**
- Customer distribution
- Revenue by customer
- Geographic analysis

**4. Product Performance**
- Top products/categories
- Sales volume analysis
- Category performance

---

## 📈 Temel Bulgular

**KPI'lar:**
-  Total Revenue: **$15.84M**
-  Total Orders: **96,470**
-  Avg Order Value: **$164.23**
-  Total Customers: **96,096**
-  Avg Review Score: **4.09/5.00**

**İçgörüler:**
- En çok gelir: São Paulo (%15.5)
- En popüler kategori: `cama_mesa_banho`
- Teslimat başarı oranı: %96
- Peak dönem: Q4 2017

---

##  Kullanılan Teknolojiler

- **Python:** Pandas, NumPy, Matplotlib, Seaborn
- **SQL:** SQLite
- **BI:** Power BI Desktop
- **Veri Kaynağı:** Kaggle
- **Version Control:** Git

---

## 🔮 Geliştirilebilecek Alanlar

### Tespit Edilen Sorunlar:

1. **CSV Format Sorunları:**
   -  Büyük veri setlerinde veri tipi kaybı
   -  Float overflow riski
   -  **Çözüm:** Parquet veya database kullanımı

2. **Veri Birleştirme Karmaşıklığı:**
   -  7 aşamalı merge işlemi hataya açık
   -  **Çözüm:** İlişkisel veritabanı + foreign keys

3. **Power BI Performansı:**
   -  200K+ satır için yavaşlama olabilir
   -  **İyileştirme:** Aggregation tabloları ekle

### Önerilen Geliştirmeler:

- [ ] **PostgreSQL/MySQL** migration (production için)
- [ ] **Incremental refresh** implementasyonu
- [ ] **Row-level security** (müşteri bazlı filtreleme)
- [ ] **Real-time dashboard** (streaming data)
- [ ] **Machine Learning:**
  - Sales forecasting (ARIMA, Prophet)
  - Customer churn prediction
  - Product recommendation engine
- [ ] **CI/CD Pipeline:**
  - Airflow ile otomatik ETL
  - Scheduled refresh
  - Data quality checks
- [ ] **Advanced Analytics:**
  - Cohort analysis
  - RFM segmentation
  - Market basket analysis

---

##  Öğrenilenler

1. **CSV yerine binary formatlar** (Parquet) veya **database kullanımı** kritik
2.  **İlişkisel model** veri bütünlüğünü ve doğruluğunu artırır
3.  **Veri tipleri** her aşamada kontrol edilmeli
4.  **Star schema** BI performansı için optimal
5.  **DAX measures** ile hesaplamalar merkezi yönetilmeli
6.  **Data validation** pipeline'ın her aşamasında yapılmalı

---

##  Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Commit yapın (`git commit -m 'Yeni özellik eklendi'`)
4. Push yapın (`git push origin feature/YeniOzellik`)
5. Pull Request açın

---

##  Lisans

Bu proje eğitim amaçlıdır. Veri seti [Olist](https://olist.com/) tarafından sağlanmıştır.

---

