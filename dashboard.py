#impor seluruh library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt
from babel.numbers import format_currency
sns.set(style='dark')

#Tahap berikutnya adalah menyiapkan DataFrame yang akan digunakan untuk membuat visualisasi data. Untuk melakukan hal ini, kita perlu membuat beberapa helper function seperti berikut. 
def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return monthly_orders_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return bystate_df

def create_rfm_df(df):
    present_day = df['order_purchase_timestamp'].max() + dt.timedelta(days=2)
    recency_df= pd.DataFrame(df.groupby(by='customer_unique_id', as_index=False)['order_purchase_timestamp'].max())
    recency_df['Recency']= recency_df['order_purchase_timestamp'].apply(lambda x: (present_day - x).days)
    
    frequency_df = pd.DataFrame(df.groupby(["customer_unique_id"]).agg({"order_id":"nunique"}).reset_index())
    frequency_df.rename(columns={"order_id":"Frequency"}, inplace=True)
    
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
#DataFrame yang telah difilter (main_df) inilah yang digunakan untuk menghasilkan berbagai DataFrame yang dibutuhkan untuk membuat visualisasi data.               
monthly_orders_df = create_monthly_orders_df(main_df)
bystate_df = create_bystate_df(main_df)
RFM_df = create_rfm_df(main_df)

##Melengkapi Dashboard dengan Berbagai Visualisasi Data
#Header
st.header('Data Analysis Dashboard :sparkles:')
#a. Sub Header (informasi tentang jumlah order bulanan ditampilkan dalam bentuk visualisasi data)
st.subheader('Monthly Orders')
 
col1, col2 = st.columns(2)
with col1:
    total_orders = monthly_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
with col2:
    total_revenue = format_currency(monthly_orders_df.revenue.sum(), "$", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_orders_df["order_purchase_timestamp"],
    monthly_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

#b. Demografi pelanggan yang kita miliki
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

#c. RFM (Recency, Frequency, & Monetary)
st.subheader("RFM Analysis")
 
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(6, 8))
plt.subplots_adjust(hspace=1)
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
sns.distplot(RFM_df['Recency'], ax=ax[0])
sns.distplot(RFM_df['Frequency'], ax=ax[1])
sns.distplot(RFM_df['Monetary'], ax=ax[2])
st.pyplot(fig)