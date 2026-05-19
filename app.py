from flask import Flask, render_template
import pandas as pd

from database.db_config import koneksi

from routes.search_routers import search_bp
from routes.recommendation_routes import recommendation_bp
from routes.history_routes import history_bp

app = Flask(__name__)
# REGISTER BLUEPRINT
app.register_blueprint(search_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(history_bp)
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
        sub_category.sub_category

    FROM product

    JOIN sub_category
    ON product.sub_category_id = sub_category.sub_category_id

    JOIN category
    ON sub_category.category_id = category.category_id

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