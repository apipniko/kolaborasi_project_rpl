from flask import Blueprint, render_template
import pandas as pd

from database.db_config import koneksi

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
def history():

    query = """
    SELECT
        users.name,
        product.product_name,
        order_items.item_price,
        orders.order_date

    FROM orders

    JOIN users
    ON orders.user_id = users.user_id

    JOIN order_items
    ON orders.order_id = order_items.order_id

    JOIN product
    ON order_items.product_id = product.product_id
    """

    df = pd.read_sql(query, koneksi)

    return render_template(
        'history.html',
        histories=df.to_dict('records')
    )