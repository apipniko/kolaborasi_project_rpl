import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database.db_config import koneksi

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
"""

df = pd.read_sql(query, koneksi)
df['tags'] = (
    df['product_name'].astype(str) + ' ' +
    df['brand'].astype(str) + ' ' +
    df['category'].astype(str) + ' ' +
    df['sub_category'].astype(str)
)
cv = CountVectorizer(stop_words='english')
vector = cv.fit_transform(df['tags']).toarray()
similarity = cosine_similarity(vector)
def get_recommendations(product_name):

    try:

        index = df[
            df['product_name'] == product_name
        ].index[0]

        distances = sorted(
            list(enumerate(similarity[index])),
            reverse=True,
            key=lambda x: x[1]
        )

        recommended_products = []

        for i in distances[1:7]:

            recommended_products.append({
                'product_id': df.iloc[i[0]].product_id,
                'product_name': df.iloc[i[0]].product_name,
                'brand': df.iloc[i[0]].brand,
                'price': df.iloc[i[0]].price,
                'category': df.iloc[i[0]].category,
                'sub_category': df.iloc[i[0]].sub_category
            })

        return recommended_products

    except:
        return []