import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Membaca dataset
product_category_translation = pd.read_csv('product_category_name_translation.csv')
products = pd.read_csv('products_dataset.csv')
sellers = pd.read_csv('sellers_dataset.csv')
order_payments = pd.read_csv('order_payments_dataset.csv')
order_reviews_dataset = pd.read_csv('order_reviews_dataset.csv')
orders = pd.read_csv('orders_dataset.csv')
geolocation = pd.read_csv('geolocation_dataset.csv')
order_items = pd.read_csv('order_items_dataset.csv')
customers = pd.read_csv('customers_dataset.csv')

# Set up layout
st.set_page_config(layout="wide")

# Dashboard title
st.title("Marketplace Data Dashboard")
st.markdown("### Dashboard Analisis Data Marketplace")

# Sidebar
st.sidebar.header("Pilih Visualisasi")
options = st.sidebar.selectbox(
    "Pilih Analisis:",
    ["Distribusi Metode Pembayaran", "Total Pendapatan per Bulan 2017"]
)

# 1. Distribusi Metode Pembayaran
if options == "Distribusi Metode Pembayaran":
    st.subheader("Distribusi Metode Pembayaran di Marketplace")
    
    # Menghitung frekuensi metode pembayaran
    payment_type_counts = order_payments['payment_type'].value_counts()

    # Membuat bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    payment_type_counts.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Distribusi Metode Pembayaran di Marketplace', fontsize=16)
    ax.set_xlabel('Metode Pembayaran', fontsize=12)
    ax.set_ylabel('Frekuensi', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# 2. Total Pendapatan per Bulan 2017
elif options == "Total Pendapatan per Bulan 2017":
    st.subheader("Total Pendapatan per Bulan di Marketplace (2017)")

    # Menggabungkan dataset orders dengan order payments
    merged_data = pd.merge(orders, order_payments, on='order_id', how='left')

    # Mengubah kolom order_purchase_timestamp menjadi tipe datetime
    merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp'], errors='coerce')

    # Menghitung total pendapatan per bulan
    monthly_revenue = merged_data.resample('M', on='order_purchase_timestamp')['payment_value'].sum().reset_index()

    # Menyiapkan rentang bulan dari awal hingga akhir
    all_months = pd.date_range(start=monthly_revenue['order_purchase_timestamp'].min(),
                                end=monthly_revenue['order_purchase_timestamp'].max(),
                                freq='M')

    # Menggabungkan dengan total pendapatan per bulan untuk memastikan semua bulan ada
    monthly_revenue = monthly_revenue.set_index('order_purchase_timestamp').reindex(all_months, fill_value=0).reset_index()
    monthly_revenue.columns = ['order_purchase_timestamp', 'payment_value']

    # Memfilter untuk tahun 2017
    monthly_revenue_2017 = monthly_revenue[monthly_revenue['order_purchase_timestamp'].dt.year == 2017]

    # Membuat visualisasi line chart untuk total pendapatan per bulan di tahun 2017
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_revenue_2017['order_purchase_timestamp'],
             monthly_revenue_2017['payment_value'],
             marker='o', color='green')
    ax.set_title('Total Pendapatan per Bulan di Marketplace (2017)', fontsize=18, fontweight='bold')
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Total Pendapatan (IDR)', fontsize=12)

    # Mengatur format angka di sumbu Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'IDR {int(x):,}'))

    # Mengatur tampilan sumbu X
    ax.set_xticks(monthly_revenue_2017['order_purchase_timestamp'])
    ax.set_xticklabels(monthly_revenue_2017['order_purchase_timestamp'].dt.strftime('%B'), rotation=45)
    ax.grid(visible=True, linestyle='--', alpha=0.7)
    st.pyplot(fig)
