from flask import Blueprint, render_template, request
import pandas as pd

from database.db_config import koneksi

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():

    query = request.args.get('query')
    category = request.args.get('category')
    sub_category = request.args.get('sub_category')

    sql = """
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
    """

    df_all = pd.read_sql(sql, koneksi)
    df = df_all.copy()

    # =========================
    # FILTER SEARCH
    # =========================

    if query and query != '':

        df = df[
            df['product_name'].str.contains(
                query,
                case=False,
                na=False
            )
        ]

    # =========================
    # FILTER CATEGORY
    # =========================

    if category and category != '':

        df = df[
            df['category'] == category
        ]

    # =========================
    # FILTER SUB CATEGORY
    # =========================

    if sub_category and sub_category != '':

        df = df[
            df['sub_category'] == sub_category
        ]

    # =========================
    # DATA FILTER DROPDOWN
    # =========================

    categories = sorted(
        df_all['category'].dropna().unique()
    )

    sub_categories = sorted(
        df_all['sub_category'].dropna().unique()
    )

    return render_template(
        'search.html',
        products=df.to_dict('records'),
        query=query,
        categories=categories,
        sub_categories=sub_categories,
        selected_category=category,
        selected_sub_category=sub_category
    )