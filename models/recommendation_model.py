import pickle
from pathlib import Path

MODEL_FILE = Path(__file__).parent / 'model_rekomendasi.pkl'

try:
    with MODEL_FILE.open('rb') as f:
        model_data = pickle.load(f)
    df = model_data.get('data')
    similarity = model_data.get('cosine_sim')
    if df is None or similarity is None:
        raise ValueError('Pickle model file does not contain expected keys: data, cosine_sim')
except Exception:
    df = None
    similarity = None


def get_recommendations(product_name):
    if df is None or similarity is None:
        return []

    try:
        product_name_lower = str(product_name).strip().lower()
        matches = df[df['product_name'].astype(str).str.lower() == product_name_lower]
        index = matches.index[0]
    except (IndexError, KeyError):
        return []

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_products = []

    for i in distances[1:7]:
        row = df.iloc[i[0]]
        recommended_products.append({
            'product_id': str(row['product_id']),
            'product_name': str(row['product_name']),
            'brand': str(row.get('brand', '')),
            'price': float(row.get('price', 0) or 0),
            'image_filename': str(row.get('image_filename', '')),
            'category': str(row.get('category', '')),
            'sub_category': str(row.get('sub_category', ''))
        })

    return recommended_products


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
