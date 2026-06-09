from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from database.db_config import koneksi

from models.recommendation_model import get_recommendations, get_search_suggestions

recommendation_bp = Blueprint(
    'recommendation',
    __name__
)

@recommendation_bp.route('/recommend/<product_name>')
def recommend(product_name):
    # 1. Ambil detail produk utama dari database
    query_main = """
        SELECT 
            p.product_id, 
            p.product_name, 
            p.brand, 
            p.price, 
            c.category, 
            sc.sub_category,
            IFNULL(COUNT(oi.product_id), 0) AS total_purchased,
            IFNULL(ROUND(AVG(u.rating), 1), 0) AS average_rating
        FROM product p
        LEFT JOIN sub_category sc ON p.sub_category_id = sc.sub_category_id
        LEFT JOIN category c ON sc.category_id = c.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        LEFT JOIN orders o ON oi.order_id = o.order_id
        LEFT JOIN users u ON o.user_id = u.user_id
        WHERE p.product_name = %s
        GROUP BY p.product_id
    """
    df_main = pd.read_sql(query_main, koneksi, params=(product_name,))
    
    # Jika produk tidak ditemukan di database, kembalikan ke home atau tampilkan error
    if df_main.empty:
        return "Produk tidak ditemukan", 404
        
    main_product = df_main.to_dict('records')[0]

    # 2. Ambil produk terkait (rekomendasi) dari Arsitektur Hybrid kita
    recommendations = get_recommendations(product_name)

    return render_template(
        'recommendation.html',
        main_product=main_product,
        recommendations=recommendations
    )

@recommendation_bp.route('/api/suggest', methods=['GET'])
def suggest_products():
    # Ambil parameter 'q' dari URL (contoh: /api/suggest?q=puzzle)
    query = request.args.get('q', '')
    
    # Dapatkan daftar produk alternatif dari model
    hasil_rekomendasi = get_search_suggestions(query)
    
    # Kembalikan hasilnya dalam bentuk JSON agar bisa dibaca JavaScript
    return jsonify(hasil_rekomendasi)