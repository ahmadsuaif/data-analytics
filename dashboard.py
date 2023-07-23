#impor seluruh library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt

sns.set(style='dark')
df= pd.read_csv('all_data.csv')
#Tahap berikutnya adalah menyiapkan DataFrame yang akan digunakan untuk membuat visualisasi data. Untuk melakukan hal ini, kita perlu membuat beberapa helper function seperti berikut.
#Q1
def create_bystate_df(df):
    bystate_df = df.customer_state.value_counts().head()
    return bystate_df

def create_bycity_df(df):
    bycity_df = df.customer_city.value_counts().head()
    return bycity_df

#Q2
def create_category_df1(df):
    category_df = df.product_category_name_english.value_counts()
    category_df1 = category_df[:5]
    return category_df1

def create_category_df2(df):
    category_df = df.product_category_name_english.value_counts()
    category_df2 = category_df[-5:]
    return category_df2

#Q3
def create_byfreight_df1(df):
    byfreight_df = df.pivot_table(index=['product_category_name_english'], values=['freight_value'],
                                         aggfunc='mean')
    byfreight_df.sort_values(by="freight_value", ascending=False)
    byfreight_df1 = byfreight_df.sort_values(by="freight_value", ascending=False).head()
    return byfreight_df1

def create_byfreight_df2(df):
    byfreight_df = df.pivot_table(index=['product_category_name_english'], values=['freight_value'],
                                         aggfunc='mean')
    byfreight_df.sort_values(by="freight_value", ascending=False)
    byfreight_df2 = byfreight_df.sort_values(by="freight_value", ascending=False).tail()
    return byfreight_df2

#Q4
def create_bysellercity_df1(df):
    bysellercity_df = df.seller_city.value_counts()
    bysellercity_df1 = bysellercity_df.head()
    return bysellercity_df1

def create_bysellercity_df2(df):
    bysellercity_df = df.seller_city.value_counts()
    bysellercity_df2 = bysellercity_df.tail()
    return bysellercity_df2

#Q5
def create_bypayment_df(df):
    bypayment_df = df['payment_type'].value_counts().reset_index()
    bypayment_df.columns = ['Payment Type', 'Count']
    bypayment_df['Percentage'] = round(bypayment_df['Count'] * 100 / bypayment_df['Count'].sum(), 2)
    return bypayment_df

#Q6-8
def create_rfm_df(df):
    present_day = df['order_purchase_timestamp'].max() + dt.timedelta(days=2)
    recency_df = pd.DataFrame(df.groupby(by='customer_unique_id', as_index=False)['order_purchase_timestamp'].max())
    recency_df['Recency'] = recency_df['order_purchase_timestamp'].apply(lambda x: (present_day - x).days)

    frequency_df = pd.DataFrame(df.groupby(["customer_unique_id"]).agg({"order_id": "nunique"}).reset_index())
    frequency_df.rename(columns={"order_id": "Frequency"}, inplace=True)

    monetary_df = df.groupby('customer_unique_id', as_index=False)['payment_value'].sum()
    monetary_df.columns = ['customer_unique_id', 'Monetary']

    RF_df = recency_df.merge(frequency_df, on='customer_unique_id')
    RFM_df = RF_df.merge(monetary_df, on='customer_unique_id').drop(columns='order_purchase_timestamp')
    return RFM_df

#Nah, setelah menyiapkan beberapa helper function tersebut, tahap berikutnya ialah load berkas all_data.csv sebagai sebuah DataFrame menggunakan kode berikut.
all_df = pd.read_csv("all_data.csv")

#Pada materi Latihan Exploratory Data Analysis, all_df memiliki dua kolom yang bertipe datetime, yaitu order_date dan delivery_date. Kolom order_date inilah yang akan menjadi kunci dalam pembuatan filter nantinya. 
datetime_columns = ["order_purchase_timestamp", "order_estimated_delivery_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

##Membuat Komponen Filter
#membuat filter dengan widget date input serta menambahkan logo perusahaan pada sidebar.
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-vector/store-staff-check-number-products-that-must-be-delivered-customers-during-day_1150-51079.jpg?w=740&t=st=1690053259~exp=1690053859~hmac=50439b02b22358b5001061e8bbcc3366c54d4e3c5da0d92291f1b68d4e365048")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
#Nah, start_date dan end_date di atas akan digunakan untuk memfilter all_df. Data yang telah difilter ini selanjutnya akan disimpan dalam main_df
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) &
                (all_df["order_purchase_timestamp"] <= str(end_date))]

##Melengkapi Dashboard dengan Berbagai Visualisasi Data
#Header
st.header('Data Analysis Dashboard :sparkles:')
bystate_df = create_bystate_df(df)
bycity_df = create_bycity_df(df)
category_df1 = create_category_df1(df)
category_df2 = create_category_df2(df)
byfreight_df1 = create_byfreight_df1(df)
byfreight_df2 = create_byfreight_df2(df)
bysellercity_df1 = create_bysellercity_df1(df)
bysellercity_df2 = create_bysellercity_df2(df)
bypayment_df = create_bypayment_df(df)
RFM_df = create_rfm_df(main_df)

#A. Demografi pelanggan
st.subheader("A. Demografi Pelanggan")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 8))
bystate_df.plot(kind='bar',title='Top 5 states with most orders',figsize=(18, 8), ax=ax[0]);
bycity_df.plot(kind='bar',title='Top 5 city with most orders',figsize=(18, 8), ax=ax[1]);
st.pyplot(fig)

#B. Kategori produk yang paling banyak dan paling sedikit
st.subheader("B. Kategori Produk")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 8))
category_df1.plot(kind='bar', title='Top 5 product category', figsize=(18, 8), ax=ax[0]);
category_df2.plot(kind='bar', title='Bottom 5 product category', figsize=(18, 8), ax=ax[1]);
st.pyplot(fig)

#C. Freight value berdasarkan kategori produk yang paling besar dan paling kecil?
st.subheader("C. Freight Value")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 8))
byfreight_df1.plot(kind='bar', title='Top 5 freight value', figsize=(18, 8), ax=ax[0]);
byfreight_df2.plot(kind='bar', title='Bottom 5 freight value', figsize=(18, 8), ax=ax[1]);
st.pyplot(fig)

#D. Kota dengan jumlah penjual terbanyak dan tersedikit
st.subheader("D. Number of Sellers")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 8))
bysellercity_df1.plot(kind='bar', title='Top 5 city with most sellers', figsize=(18, 8), ax=ax[0]);
bysellercity_df2.plot(kind='bar', title='Bottom 5 city with least sellers', figsize=(18, 8), ax=ax[1]);
st.pyplot(fig)

#E. Metode pembayaran yang paling populer dan yang paling tidak populer
st.subheader("E. Payment Methods")
fig, ax = plt.subplots(figsize=(12, 6))
labels = [credit_card', 'boleto', 'voucher', 'debit_card']
plt.pie(bypayment_df['Percentage'], labels, autopct='%1.1f%%')
plt.legend(title='Payment type Distribution');
st.pyplot(fig)

#F. RFM (Recency, Frequency, & Monetary)
st.subheader("F. RFM Analysis")

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(6, 8))
plt.subplots_adjust(hspace=1)
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
sns.distplot(RFM_df['Recency'], ax=ax[0])
sns.distplot(RFM_df['Frequency'], ax=ax[1])
sns.distplot(RFM_df['Monetary'], ax=ax[2])
st.pyplot(fig)
