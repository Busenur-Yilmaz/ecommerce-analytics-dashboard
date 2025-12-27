-- HAFTA 7 - E-COMMERCE DASHBOARD PROJECT
-- SQL ANALİZ SORGU KOLEKSIYONU
-- 1. REVENUE ANALYSIS (Gelir Analizi)

-- 1.1 Aylık Gelir Trendi
SELECT 
    order_year_month,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(SUM(price), 2) as product_revenue,
    ROUND(SUM(freight_value), 2) as freight_revenue
FROM final_merged
GROUP BY order_year_month
ORDER BY order_year_month;

-- 1.2 Çeyreksel Gelir Performansı
SELECT 
    order_year,
    order_quarter,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value
FROM final_merged
GROUP BY order_year, order_quarter
ORDER BY order_year, order_quarter;

-- 1.3 Yıllık Gelir Karşılaştırması
SELECT 
    order_year,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    COUNT(DISTINCT customer_unique_id) as unique_customers
FROM final_merged
GROUP BY order_year
ORDER BY order_year;

-- 1.4 Günlere Göre Sipariş Dağılımı
SELECT 
    order_day_of_week,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value
FROM final_merged
GROUP BY order_day_of_week
ORDER BY total_orders DESC;

-- 1.5 Saatlere Göre Sipariş Dağılımı
SELECT 
    order_hour,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue
FROM final_merged
GROUP BY order_hour
ORDER BY order_hour;

-- 2. PRODUCT ANALYSIS (Ürün Analizi)

-- 2.1 En Çok Satan Kategoriler (Top 10)
SELECT 
    product_category_name,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(order_item_id) as items_sold,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(price), 2) as avg_price,
    ROUND(AVG(avg_review_score), 2) as avg_rating
FROM final_merged
WHERE product_category_name != 'unknown'
GROUP BY product_category_name
ORDER BY total_revenue DESC
LIMIT 10;

-- 2.2 En Düşük Performanslı Kategoriler (Bottom 10)
SELECT 
    product_category_name,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(avg_review_score), 2) as avg_rating
FROM final_merged
WHERE product_category_name != 'unknown'
GROUP BY product_category_name
ORDER BY total_revenue ASC
LIMIT 10;

-- 2.3 Ürün Boyut Kategorisi Performansı
SELECT 
    product_size_category,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(AVG(delivery_time_days), 2) as avg_delivery_time
FROM final_merged
WHERE product_size_category IS NOT NULL
GROUP BY product_size_category
ORDER BY total_revenue DESC;

-- 2.4 Fiyat Aralığı Analizi
SELECT 
    CASE 
        WHEN price < 50 THEN '0-50'
        WHEN price < 100 THEN '50-100'
        WHEN price < 200 THEN '100-200'
        WHEN price < 500 THEN '200-500'
        ELSE '500+' 
    END as price_range,
    COUNT(*) as order_count,
    ROUND(SUM(total_payment_value), 2) as total_revenue
FROM final_merged
GROUP BY price_range
ORDER BY 
    CASE price_range
        WHEN '0-50' THEN 1
        WHEN '50-100' THEN 2
        WHEN '100-200' THEN 3
        WHEN '200-500' THEN 4
        ELSE 5
    END;


-- 3. CUSTOMER ANALYSIS (Müşteri Analizi)

-- 3.1 Şehirlere Göre Müşteri Dağılımı (Top 15)
SELECT 
    customer_city,
    customer_state,
    COUNT(DISTINCT customer_unique_id) as unique_customers,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value
FROM final_merged
GROUP BY customer_city, customer_state
ORDER BY total_revenue DESC
LIMIT 15;

-- 3.2 Eyaletlere Göre Müşteri Dağılımı
SELECT 
    customer_state,
    COUNT(DISTINCT customer_unique_id) as unique_customers,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(AVG(delivery_time_days), 2) as avg_delivery_time
FROM final_merged
GROUP BY customer_state
ORDER BY total_revenue DESC;

-- 3.3 Müşteri Segmentasyonu Analizi
SELECT 
    customer_segment,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(AVG(avg_review_score), 2) as avg_rating
FROM final_merged
WHERE customer_segment IS NOT NULL
GROUP BY customer_segment
ORDER BY 
    CASE customer_segment
        WHEN 'VIP' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
    END;

-- 3.4 Tekrar Eden Müşteriler
SELECT 
    customer_unique_id,
    COUNT(DISTINCT order_id) as order_count,
    ROUND(SUM(total_payment_value), 2) as lifetime_value,
    ROUND(AVG(total_payment_value), 2) as avg_order_value
FROM final_merged
GROUP BY customer_unique_id
HAVING order_count > 1
ORDER BY lifetime_value DESC
LIMIT 20;


-- 4. DELIVERY PERFORMANCE (Teslimat Performansı)

-- 4.1 Teslimat Performans Özeti
SELECT 
    delivery_performance,
    COUNT(DISTINCT order_id) as order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM final_merged), 2) as percentage,
    ROUND(AVG(delivery_time_days), 2) as avg_delivery_days
FROM final_merged
WHERE delivery_performance IS NOT NULL
GROUP BY delivery_performance
ORDER BY 
    CASE delivery_performance
        WHEN 'Early' THEN 1
        WHEN 'On Time' THEN 2
        WHEN 'Late' THEN 3
    END;

-- 4.2 Eyaletlere Göre Teslimat Performansı
SELECT 
    customer_state,
    ROUND(AVG(delivery_time_days), 2) as avg_delivery_days,
    MIN(delivery_time_days) as min_delivery_days,
    MAX(delivery_time_days) as max_delivery_days,
    COUNT(*) as total_orders,
    ROUND(SUM(CASE WHEN delivery_performance = 'Late' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as late_percentage
FROM final_merged
WHERE delivery_time_days IS NOT NULL
GROUP BY customer_state
ORDER BY avg_delivery_days DESC
LIMIT 15;

-- 4.3 Ürün Kategorisine Göre Teslimat Süresi
SELECT 
    product_category_name,
    ROUND(AVG(delivery_time_days), 2) as avg_delivery_days,
    COUNT(*) as total_orders
FROM final_merged
WHERE product_category_name != 'unknown' 
  AND delivery_time_days IS NOT NULL
GROUP BY product_category_name
ORDER BY avg_delivery_days DESC
LIMIT 15;


-- 5. PAYMENT ANALYSIS (Ödeme Analizi)

-- 5.1 Ödeme Tipi Dağılımı
SELECT 
    payment_types,
    COUNT(DISTINCT order_id) as order_count,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM final_merged), 2) as percentage
FROM final_merged
GROUP BY payment_types
ORDER BY total_revenue DESC
LIMIT 10;

-- 5.2 Taksitli Ödemeler Analizi
SELECT 
    CASE 
        WHEN has_installments = 1 THEN 'Taksitli'
        ELSE 'Peşin'
    END as payment_method,
    COUNT(DISTINCT order_id) as order_count,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(AVG(max_installments), 2) as avg_installments
FROM final_merged
WHERE has_installments IS NOT NULL
GROUP BY has_installments;

-- 5.3 Taksit Sayısına Göre Dağılım
SELECT 
    max_installments,
    COUNT(DISTINCT order_id) as order_count,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value
FROM final_merged
WHERE max_installments IS NOT NULL
GROUP BY max_installments
ORDER BY max_installments;


-- 6. SELLER ANALYSIS (Satıcı Analizi)

-- 6.1 En İyi Performans Gösteren Satıcılar (Top 20)
SELECT 
    seller_id,
    seller_seller_city,
    seller_seller_state,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(AVG(avg_review_score), 2) as avg_rating
FROM final_merged
GROUP BY seller_id, seller_seller_city, seller_seller_state
ORDER BY total_revenue DESC
LIMIT 20;

-- 6.2 Satıcıların Bulunduğu Şehirler
SELECT 
    seller_seller_city,
    seller_seller_state,
    COUNT(DISTINCT seller_id) as seller_count,
    COUNT(DISTINCT order_id) as total_orders,
    ROUND(SUM(total_payment_value), 2) as total_revenue
FROM final_merged
GROUP BY seller_seller_city, seller_seller_state
ORDER BY total_revenue DESC
LIMIT 15;

-- 7. REVIEW ANALYSIS (Yorum Analizi)

-- 7.1 Review Skor Dağılımı
SELECT 
    review_category,
    COUNT(DISTINCT order_id) as order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM final_merged WHERE review_category IS NOT NULL), 2) as percentage,
    ROUND(AVG(avg_review_score), 2) as avg_score
FROM final_merged
WHERE review_category IS NOT NULL
GROUP BY review_category
ORDER BY 
    CASE review_category
        WHEN 'Excellent' THEN 1
        WHEN 'Good' THEN 2
        WHEN 'Fair' THEN 3
        WHEN 'Poor' THEN 4
    END;

-- 7.2 Kategorilere Göre Review Skorları (En İyi 10)
SELECT 
    product_category_name,
    COUNT(*) as review_count,
    ROUND(AVG(avg_review_score), 2) as avg_rating,
    ROUND(SUM(total_payment_value), 2) as total_revenue
FROM final_merged
WHERE product_category_name != 'unknown' 
  AND avg_review_score IS NOT NULL
GROUP BY product_category_name
ORDER BY avg_rating DESC
LIMIT 10;

-- 7.3 Kategorilere Göre Review Skorları (En Kötü 10)
SELECT 
    product_category_name,
    COUNT(*) as review_count,
    ROUND(AVG(avg_review_score), 2) as avg_rating,
    ROUND(SUM(total_payment_value), 2) as total_revenue
FROM final_merged
WHERE product_category_name != 'unknown' 
  AND avg_review_score IS NOT NULL
GROUP BY product_category_name
ORDER BY avg_rating ASC
LIMIT 10;


-- 8. KPIs (Key Performance Indicators)

-- 8.1 Genel KPI'lar
SELECT 
    COUNT(DISTINCT order_id) as total_orders,
    COUNT(DISTINCT customer_unique_id) as total_customers,
    COUNT(DISTINCT product_id) as total_products,
    COUNT(DISTINCT seller_id) as total_sellers,
    COUNT(DISTINCT product_category_name) as total_categories,
    ROUND(SUM(total_payment_value), 2) as total_revenue,
    ROUND(AVG(total_payment_value), 2) as avg_order_value,
    ROUND(AVG(delivery_time_days), 2) as avg_delivery_time,
    ROUND(AVG(avg_review_score), 2) as avg_review_score
FROM final_merged;

-- 8.2 Aylık Büyüme Oranı
WITH monthly_revenue AS (
    SELECT 
        order_year_month,
        SUM(total_payment_value) as revenue
    FROM final_merged
    GROUP BY order_year_month
)
SELECT 
    order_year_month,
    ROUND(revenue, 2) as current_revenue,
    ROUND(LAG(revenue) OVER (ORDER BY order_year_month), 2) as previous_revenue,
    ROUND(((revenue - LAG(revenue) OVER (ORDER BY order_year_month)) / 
           LAG(revenue) OVER (ORDER BY order_year_month) * 100), 2) as growth_rate_percentage
FROM monthly_revenue
ORDER BY order_year_month;