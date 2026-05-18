from flask import Blueprint, render_template

from models.recommendation_model import get_recommendations

recommendation_bp = Blueprint(
    'recommendation',
    __name__
)

@recommendation_bp.route('/recommend/<product_name>')
def recommend(product_name):

    recommendations = get_recommendations(product_name)

    return render_template(
        'recommendation.html',
        product_name=product_name,
        recommendations=recommendations
    )