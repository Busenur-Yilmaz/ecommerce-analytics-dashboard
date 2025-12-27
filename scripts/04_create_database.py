"""
HAFTA 7 - E-Commerce Dashboard Project
04: SQLite Veritabanı Oluşturma

Bu script temizlenmiş CSV dosyalarını SQLite veritabanına yükler.
"""

import pandas as pd
import sqlite3
from datetime import datetime
import os

print("=" * 80)
print(" SQLITE VERİTABANI OLUŞTURMA")
print("=" * 80)

# Yollar
PROCESSED_PATH = 'data/processed/'
DATABASE_PATH = 'data/database/'
DB_FILE = f'{DATABASE_PATH}ecommerce.db'

# Database klasörünü oluştur
os.makedirs(DATABASE_PATH, exist_ok=True)

# Eğer eski database varsa sil (temiz başla)
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"\n Eski veritabanı silindi: {DB_FILE}")

# SQLite bağlantısı oluştur
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print(f"\nYeni veritabanı oluşturuldu: {DB_FILE}")

# TABLO 1: ORDERS
print("\n" + "-" * 80)
print(" ORDERS tablosu oluşturuluyor...")

orders = pd.read_csv(f'{PROCESSED_PATH}orders_clean.csv')

# Veritabanına yükle
orders.to_sql('orders', conn, if_exists='replace', index=False)

print(f"Orders tablosu oluşturuldu: {len(orders):,} satır")

# TABLO 2: CUSTOMERS
print("\n" + "-" * 80)
print("CUSTOMERS tablosu oluşturuluyor...")

customers = pd.read_csv(f'{PROCESSED_PATH}customers_clean.csv')
customers.to_sql('customers', conn, if_exists='replace', index=False)

print(f" Customers tablosu oluşturuldu: {len(customers):,} satır")

# TABLO 3: ORDER_ITEMS
print("\n" + "-" * 80)
print(" ORDER_ITEMS tablosu oluşturuluyor...")

order_items = pd.read_csv(f'{PROCESSED_PATH}order_items_clean.csv')
order_items.to_sql('order_items', conn, if_exists='replace', index=False)

print(f" Order_Items tablosu oluşturuldu: {len(order_items):,} satır")

# TABLO 4: PRODUCTS
print("\n" + "-" * 80)
print(" PRODUCTS tablosu oluşturuluyor...")

products = pd.read_csv(f'{PROCESSED_PATH}products_clean.csv')
products.to_sql('products', conn, if_exists='replace', index=False)

print(f" Products tablosu oluşturuldu: {len(products):,} satır")

# TABLO 5: SELLERS
print("\n" + "-" * 80)
print(" SELLERS tablosu oluşturuluyor...")

sellers = pd.read_csv(f'{PROCESSED_PATH}sellers_clean.csv')
sellers.to_sql('sellers', conn, if_exists='replace', index=False)

print(f" Sellers tablosu oluşturuldu: {len(sellers):,} satır")

# TABLO 6: PAYMENTS
print("\n" + "-" * 80)
print(" PAYMENTS tablosu oluşturuluyor...")

payments = pd.read_csv(f'{PROCESSED_PATH}payments_clean.csv')
payments.to_sql('payments', conn, if_exists='replace', index=False)

print(f" Payments tablosu oluşturuldu: {len(payments):,} satır")

# TABLO 7: REVIEWS
print("\n" + "-" * 80)
print(" REVIEWS tablosu oluşturuluyor...")

reviews = pd.read_csv(f'{PROCESSED_PATH}reviews_clean.csv')
reviews.to_sql('reviews', conn, if_exists='replace', index=False)

print(f" Reviews tablosu oluşturuldu: {len(reviews):,} satır")

# TABLO 8: GEOLOCATION
print("\n" + "-" * 80)
print(" GEOLOCATION tablosu oluşturuluyor...")

geolocation = pd.read_csv(f'{PROCESSED_PATH}geolocation_clean.csv')
geolocation.to_sql('geolocation', conn, if_exists='replace', index=False)

print(f" Geolocation tablosu oluşturuldu: {len(geolocation):,} satır")

# TABLO 9: FINAL_MERGED (Master Tablo)
print("\n" + "-" * 80)
print(" FINAL_MERGED (Master) tablosu oluşturuluyor...")

final_data = pd.read_csv(f'{PROCESSED_PATH}final_merged_data.csv')
final_data.to_sql('final_merged', conn, if_exists='replace', index=False)

print(f" Final_Merged tablosu oluşturuldu: {len(final_data):,} satır, {final_data.shape[1]} kolon")

# İNDEXLER OLUŞTUR (Performans için)
print("\n" + "-" * 80)
print(" İndexler oluşturuluyor (sorgu performansı için)...")

indexes = [
    "CREATE INDEX IF NOT EXISTS idx_orders_id ON orders(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id)",
    "CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_purchase_timestamp)",
    "CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id)",
    "CREATE INDEX IF NOT EXISTS idx_order_items_seller ON order_items(seller_id)",
    "CREATE INDEX IF NOT EXISTS idx_customers_id ON customers(customer_id)",
    "CREATE INDEX IF NOT EXISTS idx_customers_city ON customers(customer_city)",
    "CREATE INDEX IF NOT EXISTS idx_products_id ON products(product_id)",
    "CREATE INDEX IF NOT EXISTS idx_products_category ON products(product_category_name)",
    "CREATE INDEX IF NOT EXISTS idx_sellers_id ON sellers(seller_id)",
    "CREATE INDEX IF NOT EXISTS idx_payments_order ON payments(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_reviews_order ON reviews(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_final_order ON final_merged(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_final_customer ON final_merged(customer_id)"
]

for idx_query in indexes:
    cursor.execute(idx_query)

conn.commit()
print(f" {len(indexes)} index oluşturuldu!")

# VERİTABANI BİLGİLERİNİ GÖSTER
print("\n" + "=" * 80)
print(" VERİTABANI BİLGİLERİ")
print("=" * 80)

# Tüm tabloları listele
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"\n Toplam {len(tables)} tablo oluşturuldu:\n")

for table in tables:
    table_name = table[0]
    
    # Satır sayısını al
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    
    # Kolon sayısını al
    cursor.execute(f"PRAGMA table_info({table_name})")
    col_count = len(cursor.fetchall())
    
    print(f" {table_name:20} : {row_count:>10,} satır, {col_count:>3} kolon")

# Database dosya boyutu
db_size_mb = os.path.getsize(DB_FILE) / (1024 * 1024)
print(f"\n💾 Veritabanı boyutu: {db_size_mb:.2f} MB")

# TEST SORGUSU
print("\n" + "=" * 80)
print(" TEST SORGUSU")
print("=" * 80)

print("\n Aylık gelir trendi (Son 5 ay):\n")

test_query = """
SELECT 
    order_year_month,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value
FROM final_merged
GROUP BY order_year_month
ORDER BY order_year_month DESC
LIMIT 5
"""

result = pd.read_sql_query(test_query, conn)
print(result.to_string(index=False))

# BAĞLANTIYI KAPAT
conn.close()

print("\n" + "=" * 80)
print(" VERİTABANI BAŞARIYLA OLUŞTURULDU!")
print("=" * 80)

print(f"""
 Veritabanı Lokasyonu: {DB_FILE}
 Toplam Tablo Sayısı: {len(tables)}
 Database Boyutu: {db_size_mb:.2f} MB
 Index Sayısı: {len(indexes)}
""")