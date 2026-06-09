import os
import pickle
import pandas as pd
from database.db_config import koneksi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model_rekomendasi.pkl')


with open(MODEL_PATH, 'rb') as file:
    model_data = pickle.load(file)


cosine_sim = model_data['cosine_sim']
df = model_data['data']

def get_recommendations(nama_produk):
    """
    Fungsi untuk mendapatkan top 5 rekomendasi berdasarkan nama produk.
    """
    
    
    if nama_produk not in df['product_name'].values:
        return []  # Kembalikan list kosong jika produk tidak ditemukan di data

    # 1. Ambil index dari produk yang dicari
    idx = df[df['product_name'] == nama_produk].index[0]

    # 2. Ambil semua skor kemiripan (cosine similarity) untuk produk ini
    # enumerate digunakan untuk memasangkan index dengan skornya -> (index, skor)
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 3. Urutkan berdasarkan skor tertinggi (index ke-1 adalah skor)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 4. Ambil 5 produk teratas
    # Kita mulai dari index 1 (1:6) karena index 0 pasti produk itu sendiri (skornya 1.0)
    sim_scores = sim_scores[1:6]

    # 5. Dapatkan index baris dari 5 produk rekomendasi tersebut
    product_indices = [i[0] for i in sim_scores]

    # 6. Ambil baris data produk tersebut dari dataframe dan ubah ke bentuk list of dictionary (JSON friendly)
    rekomendasi = df.iloc[product_indices].to_dict('records')

    return rekomendasi


# ... (kode load pickle yang sebelumnya sudah ada tetap biarkan) ...

def get_search_suggestions(keyword):
    """
    Fungsi untuk mencari produk alternatif saat pengguna mengetik kata kunci.
    """
    if not keyword.strip():
        return []

    # 1. Cari produk yang namanya mengandung kata kunci (tidak sensitif huruf besar/kecil)
    # Ganti 'product_name' dengan nama kolom produk di dataframe Anda jika berbeda
    matches = df[df['product_name'].str.contains(keyword, case=False, na=False)]

    if matches.empty:
        return []

    # 2. Ambil produk pertama yang paling cocok sebagai acuan
    produk_acuan = matches.iloc[0]['product_name']

    # 3. Ambil rekomendasi alternatif untuk produk acuan tersebut
    # Menggunakan fungsi get_recommendations yang sudah kita buat sebelumnya
    alternatif_produk = get_recommendations(produk_acuan)

    return alternatif_produk



def get_popular_products():

    query = """
    SELECT
        product.product_id,
        product.product_name,
        product.brand,
        product.price,
        category.category,
        sub_category.sub_category,
        COUNT(order_items.product_id) AS total_purchased,
        ROUND(AVG(users.rating),1) AS average_rating
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

    return pd.read_sql(query, koneksi)