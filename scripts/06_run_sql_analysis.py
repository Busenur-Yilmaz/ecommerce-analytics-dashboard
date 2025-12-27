"""
HAFTA 7 - E-Commerce Dashboard Project
06: SQL Analiz Sorgularını Çalıştır ve Sonuçları Kaydet

Bu script SQL sorgularını çalıştırıp sonuçları CSV olarak kaydeder.
"""

import pandas as pd
import sqlite3
import os

print("=" * 80)
print(" SQL ANALİZ SORGUSU ÇALIŞTIRMA")
print("=" * 80)

# Veritabanı bağlantısı
DB_PATH = 'data/database/ecommerce.db'
RESULTS_PATH = 'reports/sql_results/'

# Sonuçlar klasörünü oluştur
os.makedirs(RESULTS_PATH, exist_ok=True)

# Bağlantı kur
conn = sqlite3.connect(DB_PATH)

print(f"\n Veritabanına bağlandı: {DB_PATH}")

# SQL Sorgu koleksiyonu
queries = {
    
    # REVENUE ANALYSIS
    '01_monthly_revenue': """
        SELECT 
            order_year_month,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(SUM(total_payment_value), 2) as total_revenue,
            ROUND(AVG(total_payment_value), 2) as avg_order_value
        FROM final_merged
        GROUP BY order_year_month
        ORDER BY order_year_month
    """,
    
    '02_quarterly_revenue': """
        SELECT 
            order_year,
            order_quarter,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(SUM(total_payment_value), 2) as total_revenue
        FROM final_merged
        GROUP BY order_year, order_quarter
        ORDER BY order_year, order_quarter
    """,
    
    '03_yearly_revenue': """
        SELECT 
            order_year,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(SUM(total_payment_value), 2) as total_revenue,
            COUNT(DISTINCT customer_unique_id) as unique_customers
        FROM final_merged
        GROUP BY order_year
    """,
    
    # PRODUCT ANALYSIS
    '04_top_categories': """
        SELECT 
            product_category_name,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(SUM(total_payment_value), 2) as total_revenue,
            ROUND(AVG(avg_review_score), 2) as avg_rating
        FROM final_merged
        WHERE product_category_name != 'unknown'
        GROUP BY product_category_name
        ORDER BY total_revenue DESC
        LIMIT 20
    """,
    
    '05_product_size_analysis': """
        SELECT 
            product_size_category,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(SUM(total_payment_value), 2) as total_revenue,
            ROUND(AVG(delivery_time_days), 2) as avg_delivery_time
        FROM final_merged
        WHERE product_size_category IS NOT NULL
        GROUP BY product_size_category
        ORDER BY total_revenue DESC
    """,
    
    # CUSTOMER ANALYSIS
    '06_top_cities': """
        SELECT 
            customer_city,
            customer_state,
            COUNT(DISTINCT customer_unique_id) as unique_customers,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(SUM(total_payment_value), 2) as total_revenue
        FROM final_merged
        GROUP BY customer_city, customer_state
        ORDER BY total_revenue DESC
        LIMIT 20
    """,
    
    '07_customer_segments': """
        SELECT 
            customer_segment,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(SUM(total_payment_value), 2) as total_revenue,
            ROUND(AVG(avg_review_score), 2) as avg_rating
        FROM final_merged
        WHERE customer_segment IS NOT NULL
        GROUP BY customer_segment
    """,
    
    # DELIVERY ANALYSIS
    '08_delivery_performance': """
        SELECT 
            delivery_performance,
            COUNT(DISTINCT order_id) as order_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM final_merged), 2) as percentage,
            ROUND(AVG(delivery_time_days), 2) as avg_delivery_days
        FROM final_merged
        WHERE delivery_performance IS NOT NULL
        GROUP BY delivery_performance
    """,
    
    '09_delivery_by_state': """
        SELECT 
            customer_state,
            ROUND(AVG(delivery_time_days), 2) as avg_delivery_days,
            COUNT(*) as total_orders,
            ROUND(SUM(CASE WHEN delivery_performance = 'Late' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_percentage
        FROM final_merged
        WHERE delivery_time_days IS NOT NULL
        GROUP BY customer_state
        ORDER BY avg_delivery_days DESC
        LIMIT 15
    """,
    
    # PAYMENT ANALYSIS
    '10_payment_types': """
        SELECT 
            payment_types,
            COUNT(DISTINCT order_id) as order_count,
            ROUND(SUM(total_payment_value), 2) as total_revenue,
            ROUND(AVG(total_payment_value), 2) as avg_order_value
        FROM final_merged
        GROUP BY payment_types
        ORDER BY total_revenue DESC
        LIMIT 10
    """,
    
    '11_installments': """
        SELECT 
            max_installments,
            COUNT(DISTINCT order_id) as order_count,
            ROUND(SUM(total_payment_value), 2) as total_revenue
        FROM final_merged
        WHERE max_installments IS NOT NULL
        GROUP BY max_installments
        ORDER BY max_installments
    """,
    
    # SELLER ANALYSIS
    '12_top_sellers': """
        SELECT 
            seller_id,
            seller_seller_city,
            seller_seller_state,
            COUNT(DISTINCT order_id) as total_orders,
            ROUND(SUM(total_payment_value), 2) as total_revenue,
            ROUND(AVG(avg_review_score), 2) as avg_rating
        FROM final_merged
        GROUP BY seller_id, seller_seller_city, seller_seller_state
        ORDER BY total_revenue DESC
        LIMIT 20
    """,
    
    # REVIEW ANALYSIS
    '13_review_distribution': """
        SELECT 
            review_category,
            COUNT(DISTINCT order_id) as order_count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM final_merged WHERE review_category IS NOT NULL), 2) as percentage
        FROM final_merged
        WHERE review_category IS NOT NULL
        GROUP BY review_category
    """,
    
    # KPIs
    '14_overall_kpis': """
        SELECT 
            COUNT(DISTINCT order_id) as total_orders,
            COUNT(DISTINCT customer_unique_id) as total_customers,
            COUNT(DISTINCT product_id) as total_products,
            COUNT(DISTINCT seller_id) as total_sellers,
            ROUND(SUM(total_payment_value), 2) as total_revenue,
            ROUND(AVG(total_payment_value), 2) as avg_order_value,
            ROUND(AVG(delivery_time_days), 2) as avg_delivery_time,
            ROUND(AVG(avg_review_score), 2) as avg_review_score
        FROM final_merged
    """
}

print(f"\n {len(queries)} adet sorgu çalıştırılacak...\n")

# Her sorguyu çalıştır ve kaydet
for query_name, query in queries.items():
    try:
        print(f" {query_name} çalıştırılıyor...")
        
        # Sorguyu çalıştır
        df = pd.read_sql_query(query, conn)
        
        # CSV olarak kaydet
        output_file = f'{RESULTS_PATH}{query_name}.csv'
        df.to_csv(output_file, index=False)
        
        print(f"    Kaydedildi: {output_file} ({len(df)} satır, {len(df.columns)} kolon)")
        
        # İlk birkaç satırı göster
        if len(df) <= 5:
            print(f"\n{df.to_string(index=False)}\n")
        
    except Exception as e:
        print(f"    HATA: {str(e)}\n")

# Bağlantıyı kapat
conn.close()

print("\n" + "=" * 80)
print(" TÜM SQL ANALİZLERİ TAMAMLANDI!")
print("=" * 80)

print(f"""
 Sonuçlar kaydedildi: {RESULTS_PATH}
 Toplam sorgu: {len(queries)}
 Oluşturulan CSV dosyası: {len(queries)}
""")