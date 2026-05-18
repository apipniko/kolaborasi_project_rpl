from flask import Blueprint, render_template, request
import pandas as pd

from database.db_config import koneksi

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():

    query = request.args.get('query')

    sql = """
    SELECT
        product.product_id,
        product.product_name,
        product.brand,
        product.price,
        category.category,
        sub_category.sub_category

    FROM product

    JOIN sub_category
    ON product.sub_category_id = sub_category.sub_category_id

    JOIN category
    ON sub_category.category_id = category.category_id
    """

    df = pd.read_sql(sql, koneksi)

    if query:

        result = df[
            df['product_name'].str.contains(
                query,
                case=False,
                na=False
            )
        ]

    else:
        result = df

    return render_template(
        'search.html',
        products=result.to_dict('records'),
        query=query
    )