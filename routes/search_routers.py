from flask import Blueprint, render_template, request
import pandas as pd

from database.db_config import koneksi

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    query = request.args.get('query', '').strip()
    category = request.args.get('category', '').strip()
    sub_category = request.args.get('sub_category', '').strip()
    sort_by = request.args.get('sort', 'relevant')

    # Query disesuaikan & LIMIT dihapus agar filter/sort bisa berjalan dinamis
    sql = """
    SELECT
        product.product_id,
        product.product_name,
        product.brand,
        product.price,
        category.category,
        sub_category.sub_category,
        COUNT(order_items.product_id) AS total_purchased,
        ROUND(AVG(users.rating), 1) AS average_rating
    FROM product
    JOIN sub_category ON product.sub_category_id = sub_category.sub_category_id
    JOIN category ON sub_category.category_id = category.category_id
    LEFT JOIN order_items ON product.product_id = order_items.product_id
    LEFT JOIN orders ON order_items.order_id = orders.order_id
    LEFT JOIN users ON orders.user_id = users.user_id
    GROUP BY 
        product.product_id, 
        product.product_name, 
        product.brand, 
        product.price, 
        category.category, 
        sub_category.sub_category
    """

    df_all = pd.read_sql(sql, koneksi)
    df = df_all.copy()

    # =========================
    # FILTER LOGIC
    # =========================
    if query:
        df = df[df['product_name'].str.contains(query, case=False, na=False)]
    if category:
        df = df[df['category'] == category]
    if sub_category:
        df = df[df['sub_category'] == sub_category]

    # =========================
    # SORTING LOGIC (PANDAS)
    # =========================
    if sort_by == 'highest_rating':
        df = df.sort_values(by='average_rating', ascending=False, na_position='last')
    elif sort_by == 'lowest':
        df = df.sort_values(by='price', ascending=True)
    elif sort_by == 'most_purchased':
        df = df.sort_values(by='total_purchased', ascending=False)
    else:  # 'relevant' / default
        df = df.sort_values(by='total_purchased', ascending=False)

    # Optional: Batasi tampilan maksimal 12 produk SETELAH filter & sort
    # df = df.head(12)

    # =========================
    # DROPDOWN OPTIONS
    # =========================
    categories = sorted(df_all['category'].dropna().unique())
    sub_categories = sorted(df_all['sub_category'].dropna().unique())

    return render_template(
        'search.html',
        products=df.to_dict('records'),
        query=query,
        categories=categories,
        sub_categories=sub_categories,
        selected_category=category,
        selected_sub_category=sub_category
    )