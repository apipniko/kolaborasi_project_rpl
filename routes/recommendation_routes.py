from flask import Blueprint, render_template,request, jsonify

from database.db_config import koneksi
from models.recommendation_model import get_recommendations, get_search_suggestions

recommendation_bp = Blueprint(
    'recommendation',
    __name__
)


def get_product(product_name):
    cursor = koneksi.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            product.product_id,
            product.product_name,
            product.brand,
            product.price,
            product.image_filename,
            category.category,
            sub_category.sub_category
        FROM product
        JOIN sub_category
        ON product.sub_category_id = sub_category.sub_category_id
        JOIN category
        ON sub_category.category_id = category.category_id
        WHERE product.product_name = %s
        LIMIT 1
        """,
        (product_name,)
    )
    product = cursor.fetchone()
    cursor.close()
    return product

@recommendation_bp.route('/recommend/<product_name>')
def recommend(product_name):

    recommendations = get_recommendations(product_name)
    product = get_product(product_name)

    return render_template(
        'recommendation.html',
        product=product,
        product_name=product_name,
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