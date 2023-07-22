# -*- coding: utf-8 -*-
"""Submission Belajar Analisis Data - Ahmad Suaif

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dg082IHcaCA_hPkDBwjyPoUe7hfR7lV3

# Proyek Analisis Data: Nama dataset
- Nama: Ahmad Suaif
- Email: ahmadsuaif@gmail.com
- Id Dicoding:ahmadsuaif

## Menentukan Pertanyaan Bisnis

- Pertanyaan 1: Bagaimana Performa Penjualan dan Revenue Perusahaan dalam Beberapa Bulan Terakhir?
- Pertanyaan 2: Bagaimana Demografi Pelanggan yang Kita Miliki?
- Pertanyaan 3: Kapan terakhir pelanggan melakukan transaksi?
- Pertanyaan 4: Seberapa sering seorang pelanggan melakukan pembelian dalam beberapa bulan terakhir?
- Pertanyaan 5: Berapa banyak uang yang dihabiskan pelanggan dalam beberapa bulan terakhir?

## Menyiapkan semua library yang dibuthkan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

"""## Data Wrangling

### Gathering Data
"""

from google.colab import drive
drive.mount('/content/drive')

customers_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/customers_dataset.csv')
geolocation_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/geolocation_dataset.csv')
items_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/order_items_dataset.csv')
payments_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/order_payments_dataset.csv')
reviews_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/order_reviews_dataset.csv')
orders_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/orders_dataset.csv')
products_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/products_dataset.csv')
sellers_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/sellers_dataset.csv')
category_translation_df= pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Dicoding - Belajar Analisis Data dengan Python/E-Commerce Public Dataset/product_category_name_translation.csv')

customers_df

geolocation_df

items_df

payments_df

reviews_df

orders_df

products_df

sellers_df

category_translation_df

"""### Assessing Data"""

datasets = [customers_df, geolocation_df, items_df, payments_df, reviews_df, orders_df, products_df, sellers_df, category_translation_df]
titles = ["customers", "geolocation", "items", "payments", "reviews", "orders", "products", "sellers", "category_translation"]

data_summary = pd.DataFrame({},)
data_summary['datasets']= titles
data_summary['columns'] = [', '.join([col for col, null in data.isnull().sum().items() ]) for data in datasets]
data_summary['total_rows']= [data.shape[0] for data in datasets]
data_summary['total_cols']= [data.shape[1] for data in datasets]
data_summary['total_duplicate']= [len(data[data.duplicated()]) for data in datasets]
data_summary['total_null']= [data.isnull().sum().sum() for data in datasets]
data_summary['null_cols'] = [', '.join([col for col, null in data.isnull().sum().items() if null > 0]) for data in datasets]
data_summary.style.background_gradient()

"""### Cleaning Data

Secara garis besar, terdapat tiga metode dalam mengatasi missing value antara lain seperti berikut:
- Dropping
- Imputation
- Interpolation
"""

for i in datasets:
    i.dropna(inplace=True)

for i in datasets:
    i.drop(i[i.duplicated()].index, axis=0, inplace=True)

data_summary = pd.DataFrame({},)
data_summary['datasets']= titles
data_summary['columns'] = [', '.join([col for col, null in data.isnull().sum().items() ]) for data in datasets]
data_summary['total_rows']= [data.shape[0] for data in datasets]
data_summary['total_cols']= [data.shape[1] for data in datasets]
data_summary['total_duplicate']= [len(data[data.duplicated()]) for data in datasets]
data_summary['total_null']= [data.isnull().sum().sum() for data in datasets]
data_summary['null_cols'] = [', '.join([col for col, null in data.isnull().sum().items() if null > 0]) for data in datasets]
data_summary.style.background_gradient()

for i in datasets:
    i.info()

merged_df= pd.merge(customers_df, orders_df, on="customer_id")
merged_df= merged_df.merge(reviews_df, on="order_id")
merged_df= merged_df.merge(items_df, on="order_id")
merged_df= merged_df.merge(products_df, on="product_id")
merged_df= merged_df.merge(payments_df, on="order_id")
merged_df= merged_df.merge(sellers_df, on='seller_id')
merged_df= merged_df.merge(category_translation_df, on='product_category_name')
merged_df

merged_df.isnull().sum()

merged_df.duplicated().sum()

merged_df.info()

"""Selain itu kita perlu melakukan konversi tipe data"""

time_columns= ['order_purchase_timestamp', 'order_approved_at','order_delivered_carrier_date','order_delivered_customer_date',
               'order_estimated_delivery_date', 'review_creation_date', 'review_answer_timestamp', 'shipping_limit_date']

merged_df[time_columns]=merged_df[time_columns].apply(pd.to_datetime)
merged_df.info()

"""## Exploratory Data Analysis (EDA)

### Explore ...

a. Customer Exploratory
"""

merged_df.groupby(by="customer_city").customer_id.nunique().sort_values(ascending=False)

merged_df.groupby(by="customer_state").customer_id.nunique().sort_values(ascending=False)

"""a. Order Exploratory"""

delivery_time = merged_df["order_estimated_delivery_date"] - merged_df["order_approved_at"]
delivery_time = delivery_time.apply(lambda x: x.total_seconds())
orders_df["delivery_time"] = round(delivery_time/86400)
orders_df

orders_df.describe(include="all")

"""c. Customer & Order Exploratory"""

orders_customers_df = pd.merge(
    left=orders_df,
    right=customers_df,
    how="left",
    left_on="customer_id",
    right_on="customer_id"
)
orders_customers_df.head()

# Jumlah order berdasarkan kota

orders_customers_df.groupby(by="customer_city").order_id.nunique().sort_values(ascending=False).reset_index().head(10)

# Jumlah order berdasarkan state

orders_customers_df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=False)

"""## Visualization & Explanatory Analysis

### Pertanyaan 1:

Bagaimana Performa Penjualan dan Revenue Perusahaan dalam Beberapa Bulan Terakhir?
"""

monthly_orders_df = merged_df.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",
    "price": "sum"
})
monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
monthly_orders_df = monthly_orders_df.reset_index()
monthly_orders_df.rename(columns={
    "order_id": "order_count",
    "price": "revenue"
}, inplace=True)
monthly_orders_df

plt.figure(figsize=(10, 5))
plt.plot(
    monthly_orders_df["order_purchase_timestamp"],
    monthly_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="blue"
)
plt.title("Number of Orders per Month (2017-2018)", loc="center", fontsize=20)
plt.xticks(fontsize=10)
plt.xticks(rotation=45)
plt.yticks(fontsize=10)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(
    monthly_orders_df["order_purchase_timestamp"],
    monthly_orders_df["revenue"],
    marker='o',
    linewidth=2,
    color="blue"
)
plt.title("Total Revenue per Month (2017-2018)", loc="center", fontsize=20)
plt.xticks(fontsize=10)
plt.xticks(rotation=45)
plt.yticks(fontsize=10)
plt.show()

"""### Pertanyaan 2:

Bagaimana Demografi Pelanggan yang Kita Miliki?
"""

bystate_df = merged_df.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={
    "customer_id": "customer_count"
}, inplace=True)
bystate_df
plt.figure(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors_
)
plt.title("Number of Customer by States", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
plt.show()

"""### Pertanyaan 3, 4, dan 5:

- Kapan terakhir pelanggan melakukan transaksi?
- Seberapa sering seorang pelanggan melakukan pembelian dalam beberapa bulan terakhir?
- Berapa banyak uang yang dihabiskan pelanggan dalam beberapa bulan terakhir?

Untuk menjawab tiga pertanyaan analisis terakhir, kita bisa menggunakan teknik analisis lanjutan yang bernama RFM analysis. Sederhananya, RFM analysis merupakan salah satu metode yang umum digunakan untuk melakukan segmentasi pelanggan (mengelompokkan pelanggan ke dalam beberapa kategori) berdasarkan tiga parameter, yaitu **recency, frequency, dan monetary.**

RFM analysis adalah proses segmentasi pelanggan secara efektif dengan mempertimbangkan recency, frequency, dan monetary value.

a. Recency
"""

present_day = merged_df['order_purchase_timestamp'].max() + dt.timedelta(days=2)
present_day

print("Latest date in dataset: ", merged_df['order_purchase_timestamp'].max())

recency_df= pd.DataFrame(merged_df.groupby(by='customer_unique_id', as_index=False)['order_purchase_timestamp'].max())
recency_df

recency_df['Recency']= recency_df['order_purchase_timestamp'].apply(lambda x: (present_day - x).days)
recency_df

"""b. Frequency"""

frequency_df = pd.DataFrame(merged_df.groupby(["customer_unique_id"]).agg({"order_id":"nunique"}).reset_index())
frequency_df.rename(columns={"order_id":"Frequency"}, inplace=True)
frequency_df

"""c. Monetary"""

monetary_df = merged_df.groupby('customer_unique_id', as_index=False)['payment_value'].sum()
monetary_df.columns = ['customer_unique_id', 'Monetary']
monetary_df

RF_df = recency_df.merge(frequency_df, on='customer_unique_id')
RFM_df = RF_df.merge(monetary_df, on='customer_unique_id').drop(columns='order_purchase_timestamp')
RFM_df

RFM_df.describe()

plt.figure(figsize=(12, 10))
plt.subplot(3, 1, 1); sns.distplot(RFM_df['Recency'])
plt.subplot(3, 1, 2); sns.distplot(RFM_df['Frequency'])
plt.subplot(3, 1, 3); sns.distplot(RFM_df['Monetary'])
plt.show()

"""## Conclusion

- Kesimpulan Pertanyaan 1: Performa penjualan cenderung naik dengan jumlah penjualan terbanyak pada Mei 2018 sebanyak 2171 dengan pendapatan sebesar 368100.77
- Kesimpulan Pertanyaan 2: Pelanggan terbanyak berasal dari SP, RI, MG, dan seterusnya
- Kesimpulan Pertanyaan 3: Transaksi terakhir tercatat pada 2018-08-29 14:18:28
- Kesimpulan Pertanyaan 4: Rata-rata pelanggan melakukan sebanyak 1 kali. Namun tercatat ada pelanggan yang melakukan 3 kali transaksi.
- Kesimpulan Pertanyaan 5: Rata-rata pelanggan menghabiskan uang sebesar 245 dengan nilai terbesar yaitu 29099.52
"""

