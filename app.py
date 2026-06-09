from flask import Flask, render_template
import pandas as pd
from dotenv import load_dotenv
from database.db_config import koneksi
import os
import mysql.connector 
from routes.search_routers import search_bp
from routes.recommendation_routes import recommendation_bp
from routes.history_routes import history_bp
from models.recommendation_model import get_popular_products\


load_dotenv()


app = Flask(__name__)




# REGISTER BLUEPRINT
app.register_blueprint(search_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(history_bp)
# HOME

@app.route('/')
def home():
    df = get_popular_products()

    return render_template(
        'index.html',
        products=df.to_dict('records')
    )
# RUN FLASK
if __name__ == '__main__':
    app.run(debug=True)