import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

with st.sidebar:
    st.title('Analisis Data E-commerce')

    st.markdown(
    """
    1. Lihat Kategori Produk Terlaris
    2. Lihat Kategori Produk dengan Semua Rating
    """
)
base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, "category_tren.csv")
category_tren_df = pd.read_csv(file_path)


product_category = pd.read_csv(os.path.join(base_path, "product_category_name_translation.csv"))
# Konversi kolom 'shipping_limit_date' menjadi datetime
category_tren_df['shipping_limit_date'] = pd.to_datetime(category_tren_df['shipping_limit_date'])

st.title("Analisis Kategori Produk yang Sangat Laris Tiap Tahunnya!")

# Tambahkan input tahun
selected_year = st.number_input('Pilih Tahun Terlebih Dahulu', min_value=2016, max_value=2020, value=2018, step=1)

order_selected_year = (category_tren_df['shipping_limit_date'].dt.year == selected_year)
order_selected_year = category_tren_df[order_selected_year]

most_ordered_in_year = order_selected_year.groupby(['product_category_name']).size().reset_index(name='count')
most_ordered_in_year_sorted = most_ordered_in_year.sort_values(by='count', ascending=False)

most_ordered_categories = pd.merge(most_ordered_in_year_sorted, product_category, on='product_category_name', how='inner')

most_ordered_categories.index = most_ordered_categories.index + 1

# Memilih kolom yang ingin ditampilkan
selected_columns = ['product_category_name_english', 'count']

# Mengambil hanya 5 kategori teratas
top_5_categories = most_ordered_categories.head(5)

# Menampilkan bar plot kategori produk terbanyak pada tahun yang dipilih (5 teratas)
plt.figure(figsize=(10, 6))
plt.barh(top_5_categories['product_category_name_english'], top_5_categories['count'], color='blue', alpha=0.7)
plt.xlabel('Jumlah Pesanan')
plt.ylabel('Kategori Produk')
plt.title(f'5 Kategori Produk Terbanyak pada Tahun {selected_year}')
plt.tight_layout()

# Menampilkan plot ke aplikasi Streamlit
st.pyplot(plt)

order_reviews_df = pd.read_csv(os.path.join(base_path, "order_reviews_clean.csv"))


# Definisikan fungsi untuk melihat kategori produk dengan rating score 5 terbanyak
def best_review_categories():
    st.title("Analisis Kategori Produk dengan Rating Terbaik")

    selected_rating = st.multiselect('Pilih Peringkat Produk', [1, 2, 3, 4, 5], default=[5])

    best_review = order_reviews_df[order_reviews_df['review_score'].isin(selected_rating)]
    best_review = pd.merge(best_review, product_category,
                           left_on='product_category_name_x',
                           right_on='product_category_name', how='inner')

    # Group by rating dan kategori
    best_review = best_review.groupby(['review_score', 'product_category_name_english']).size().reset_index(name='count')

    # Ambil 5 teratas per rating
    top_reviews = (
        best_review.groupby('review_score', group_keys=False)
        .apply(lambda x: x.sort_values('count', ascending=False).head(5))
    )

    if top_reviews.empty:
        st.warning("Data tidak ditemukan untuk rating yang dipilih.")
        return

    # Mapping warna berdasarkan rating
    color_map = {1: 'red', 2: 'orange', 3: 'yellow', 4: 'blue', 5: 'green'}
    bar_colors = top_reviews['review_score'].map(color_map).fillna('gray')

    # Buat plot horizontal
    plt.figure(figsize=(10, 6))
    plt.barh(top_reviews['product_category_name_english'],
             top_reviews['count'],
             color=bar_colors,
             alpha=0.8)

    plt.xlabel('Jumlah Produk')
    plt.ylabel('Kategori Produk')
    plt.title(f'Kategori Produk dengan Rating {selected_rating}')
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=f'Rating {score}')
                    for score, color in color_map.items() if score in selected_rating]
    plt.legend(handles=legend_elements)
    plt.tight_layout()
    st.pyplot(plt)

# Panggil fungsi best_review_categories() untuk menjalankannya
best_review_categories()

st.caption('Copyright (c) MHD Anwar 2025')