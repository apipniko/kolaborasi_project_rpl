# Sistem Rekomendasi Produk Mainan

## Deskripsi
Project ini merupakan sistem rekomendasi produk mainan berbasis web menggunakan Flask dan MySQL. Sistem dapat melakukan pencarian produk serta memberikan rekomendasi produk berdasarkan kategori, sub kategori, brand, dan nama produk menggunakan metode Content Based Filtering dan Cosine Similarity.

---

## Fitur Sistem

- Melihat produk
- Searching produk
- Filter kategori dan sub kategori
- Recommendation system
- Riwayat pembelian

---

## Teknologi Yang Digunakan

### Backend
- Python Flask

### Frontend
- HTML
- Tailwind CSS
- Jinja2

### Database
- MySQL

### Machine Learning
- Content Based Filtering
- Cosine Similarity

---

## Struktur Project

```text
recommendation-system/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
├── models/
├── routes/
├── templates/
├── static/
└── assets/
```

---

## Cara Menjalankan Project

### 1. Install Library

```bash
pip install -r requirements.txt
```

---

### 2. Jalankan MySQL

Nyalakan:
- Apache
- MySQL

---

### 3. Import Database

Import file:

```text
toy_recommendation_database.sql
```

ke phpMyAdmin atau SQLyog.

---

### 4. Jalankan Flask

```bash
python app.py
```

---

### 5. Buka Browser

```text
http://127.0.0.1:5000
```

---

## Metode Recommendation System

Sistem rekomendasi menggunakan metode:

- Content Based Filtering
- CountVectorizer
- Cosine Similarity

Sistem akan merekomendasikan produk berdasarkan:
- nama produk
- kategori
- sub kategori
- brand

---

## Author

Nama: (Isi Nama Kamu)