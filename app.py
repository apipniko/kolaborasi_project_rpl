import os

from flask import Flask, render_template
import pandas as pd

from database.db_config import koneksi

from routes.search_routers import search_bp
from routes.recommendation_routes import recommendation_bp
from routes.history_routes import history_bp
from routes.purchase_routes import purchase_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'toy-recommendation-dev-secret')


@app.template_filter('currency')
def currency(value):
    try:
        amount = float(value)
        if amount.is_integer():
            formatted = f"{int(amount):,}".replace(',', '.')
        else:
            formatted = f"{amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"$ {formatted}"
    except Exception:
        return value


# REGISTER BLUEPRINT
app.register_blueprint(search_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(history_bp)
app.register_blueprint(purchase_bp)
# HOME
@app.route('/')
def home():

    query = """
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

    JOIN sub_category
    ON product.sub_category_id = sub_category.sub_category_id

    JOIN category
    ON sub_category.category_id = category.category_id

    LEFT JOIN order_items
    ON product.product_id = order_items.product_id

    LEFT JOIN orders
    ON order_items.order_id = orders.order_id

    LEFT JOIN users
    ON orders.user_id = users.user_id

    GROUP BY product.product_id

    ORDER BY total_purchased DESC

    LIMIT 12
    """

    df = pd.read_sql(query, koneksi)

    return render_template(
        'index.html',
        products=df.to_dict('records')
    )
# RUN FLASK
if __name__ == '__main__':
    app.run(debug=True)
