import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import numpy as np

# Mendapatkan path direktori saat ini
current_dir = os.path.dirname(os.path.abspath(__file__))

# Fetch Data
day_csv_path = os.path.join(current_dir, "bike_sharing_day_df.csv")
hour_csv_path = os.path.join(current_dir, "bike_sharing_hour_df.csv")

bs_days_df = pd.read_csv(day_csv_path)
bs_hours_df = pd.read_csv(hour_csv_path)
# Function


def count_day_df(bs_day_df):
    bs_day_df_count = bs_day_df.groupby('day', observed=True)[
        'count'].sum().reset_index()
    return bs_day_df_count


def sum_registered_df(bs_day_df):
    registered_df_sum = bs_day_df.groupby(by="date").agg({
        "registered": "sum"
    })
    registered_df_sum = registered_df_sum.reset_index()
    registered_df_sum.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
    return registered_df_sum


def sum_casual_df(bs_day_df):
    casual_df_sum = bs_day_df.groupby(by="date").agg({"casual": "sum"})
    casual_df_sum = casual_df_sum.reset_index()
    casual_df_sum.rename(columns={"casual": "casual_sum"}, inplace=True)
    return casual_df_sum


# Dashboard
style_path = os.path.join(current_dir, "style.css")
st.set_page_config(page_title="Bike Sharing Dashboard",
                   page_icon="🚴", layout="wide")
with open(style_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.subheader("Bike Sharing Data Analytics🚴")


# Konversi kolom 'date' ke tipe datetim
datetime_columns = ["date"]
bs_days_df.sort_values(by="date", inplace=True)
bs_days_df.reset_index(inplace=True)

bs_hours_df.sort_values(by="date", inplace=True)
bs_hours_df.reset_index(inplace=True)

for column in datetime_columns:
    bs_days_df[column] = pd.to_datetime(bs_days_df[column])
    bs_hours_df[column] = pd.to_datetime(bs_hours_df[column])

min_date_days = bs_days_df["date"].min()
max_date_days = bs_days_df["date"].max()

min_date_hour = bs_hours_df["date"].min()
max_date_hour = bs_hours_df["date"].max()

# Sidebar
with st.sidebar:
    # Logo
    st.image("https://i.pinimg.com/736x/d2/8a/cf/d28acf46849e282e44a1ed60cf8a3d0c.jpg")

    # start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

main_bs_days_df = bs_days_df[(bs_days_df["date"] >= str(start_date)) &
                             (bs_days_df["date"] <= str(end_date))]

main_bs_hours_df = bs_hours_df[(bs_hours_df["date"] >= str(start_date)) &
                               (bs_hours_df["date"] <= str(end_date))]

st.sidebar.markdown('''
---
Dicoding: Daniela N.
''')

# Menghitung data berdasarkan filter
bs_day_df_count = count_day_df(main_bs_days_df)
registered_df_sum = sum_registered_df(main_bs_days_df)
casual_df_sum = sum_casual_df(main_bs_days_df)

# Row A
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    sum_order = bs_day_df_count['count'].sum()
    st.markdown(
        f"""
        <div class="card">
            <p class="label">Jumlah Total Pengguna Sepeda</p>
            <p class="value">{sum_order}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    sum_registered = registered_df_sum.register_sum.sum()
    st.markdown(
        f"""
        <div class="card">
            <p class="label">Jumlah Total Pengguna Sepeda 'Registered'</p>
            <p class="value">{sum_registered}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    sum_casual = casual_df_sum.casual_sum.sum()
    st.markdown(
        f"""
        <div class="card">
            <p class="label">Jumlah Total Pengguna Sepeda 'Casual'</p>
            <p class="value">{sum_casual}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown('##')
# Row B
st.subheader('Berapa perbandingan dan persentase pengguna yang merupakan pelanggan terdaftar (registered) dibandingkan pengguna kasual (casual)?')
c1, c2 = st.columns((7, 3))
with c1:
    st.markdown('### Perbandingan')
    hue_order = ['Weekend', 'Weekday']

    fig, (ax1, ax2) = plt.subplots(figsize=(20, 10), nrows=2)

    sns.lineplot1 = sns.lineplot(x='hour', y='casual', hue='day_type',
                                 hue_order=hue_order, palette='bright', data=bs_hours_df, ax=ax1)
    ax1.set_title(
        'Distribution of casual users per hour based on workday', fontsize=15)
    ax1.set_xlabel('Hour', fontsize=15)
    ax1.set_xticks(range(0, 24))
    ax1.set_ylabel('Casual users', fontsize=15)

    handles, labels = ax1.get_legend_handles_labels()

    ax1.legend(handles=handles, labels=['Yes', 'No'], loc='upper right', fontsize=15,
               title='Workday', title_fontsize=15, facecolor='lightgray', framealpha=0.8)

    sns.lineplot2 = sns.lineplot(x='hour', y='registered', hue='day_type',
                                 hue_order=hue_order, palette='bright', data=bs_hours_df, ax=ax2)
    ax2.set_title(
        'Distribution of registered users per hour based on workday', fontsize=15)
    ax2.set_xlabel('Hour', fontsize=15)
    ax2.set_xticks(range(0, 24))
    ax2.set_ylabel('Registered users', fontsize=15)

    st.pyplot(fig)


with c2:
    st.markdown('### Presentase')
    total_registered = bs_days_df['registered'].sum()
    total_casual = bs_hours_df['casual'].sum()
    labels = ['Registered', 'Casual']
    sizes = [total_registered, total_casual]
    colors = ['skyblue', 'orange']

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, colors=colors,
           autopct='%1.1f%%', startangle=140, pctdistance=0.85)
    ax.axis('equal')
    ax.set_title('Percentage of Registered vs Casual Customer')
    st.pyplot(fig)

st.markdown('##')
# Row C
st.subheader(
    'Bagaimana performa peminjaman sepeda perbulan pada tahun 2011 hingga 2012?')

hour_df = bs_hours_df[['date', 'year', 'month', 'hour', 'day',
                       'season', 'weather', 'count', 'registered', 'casual']]
monthly_rentals = hour_df.groupby(['year', 'month'], observed=True)[
    ['count', 'registered', 'casual']].sum().reset_index()

monthly_rentals = monthly_rentals[[
    'year', 'month', 'count', 'registered', 'casual']]

print(monthly_rentals)

# Convert 'year' and 'month' to string and concatenate them
monthly_rentals['time'] = monthly_rentals['year'].astype(
    str) + '-' + monthly_rentals['month'].astype(str)

# Convert 'time' to datetime
monthly_rentals['datetime'] = pd.to_datetime(
    monthly_rentals['time'], format='%Y-%B')

# Sort by 'date'
monthly_rentals = monthly_rentals.sort_values('datetime')

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_rentals['datetime'], monthly_rentals['count'],
        marker='o', label='Total Rentals (count)', color='#90CAF9')
ax.set_title('Monthly Bike Rentals Over Two Years')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Rentals')
ax.legend()
plt.xticks(rotation=45)
plt.grid(True)

# Tampilkan plot di Streamlit
st.pyplot(fig)

st.markdown('##')
# Row D
st.subheader(
    ' Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?')

# Mengelompokkan data berdasarkan kolom 'season' dan menjumlahkan kolom 'count'
season_count = bs_days_df.groupby('season', observed=True)[
    'count'].sum().reset_index()

data = season_count['count'].values
labels = season_count['season'].astype(str)  # Mengubah indeks season ke string

# Menampilkan pie plot
ax.set_title('Persentase Jumlah Pengguna Berdasarkan Season')

fig, ax = plt.subplots(figsize=(10, 6))

# Membuat pie plot dengan persentase
ax.pie(data, labels=labels, autopct='%1.1f%%', colors=[
       "#E6324C", "#72BCD4", "#D6AF08", "#C70578"])
ax.set_title('Persentase Jumlah Pengguna Berdasarkan Season')

# Menambahkan tabel di sebelah kanan pie chart
table_data = season_count.values  # Mengambil nilai tabel
table = plt.table(cellText=table_data,
                  colLabels=['Season', 'Count'],
                  cellLoc='center',
                  loc='right',
                  # Mengatur posisi dan ukuran tabel
                  bbox=[1.25, 0.1, 0.5, 0.8])

# Menampilkan tabel
table.auto_set_font_size(False)
table.set_fontsize(12)

# Tampilkan grafik di Streamlit
st.pyplot(fig)

st.markdown('##')
# Row D
st.subheader(
    ' Pada jam berapa penggunaan sepeda mencapai puncaknya dalam sehari?')

# Daftar semua hari dalam seminggu
days_of_week = ["Days of the Week", "Monday", "Tuesday",
                "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Layout dengan kolom untuk dropdown dan grafik
col1, col2 = st.columns([1, 4])

with col1:
    selected_day = st.selectbox(
        'Select Day:',
        options=days_of_week,
        index=0
    )

# Filter data berdasarkan pilihan pengguna
if selected_day == "Days of the Week":
    filtered_data = bs_hours_df
else:
    filtered_data = bs_hours_df[bs_hours_df['day'] == selected_day]

with col2:
    # Visualisasi menggunakan Seaborn
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))

    sns.lineplot(
        data=filtered_data,
        x='hour',
        y='count',
        hue='day',
        palette='Set2',
        linewidth=2.5,
        marker="o"
    )

    plt.title('Tren Penggunaan Sepeda Berdasarkan Jam dalam Sehari',
              fontsize=14, fontweight='bold')
    plt.xlabel('Jam dalam Sehari', fontsize=12)
    plt.ylabel('Jumlah Sepeda yang Digunakan (count)', fontsize=12)
    plt.xticks(np.arange(0, 24, 1))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(title="Hari", bbox_to_anchor=(
        1.05, 1), loc='upper left', fontsize=10)

    # Tampilkan plot di Streamlit
    st.pyplot(plt)

bins = [bs_hours_df['atemp'].min(), 0.25, 0.75, bs_hours_df['atemp'].max()]
labels = ['Cold', 'Mild', 'Hot']

bs_hours_df['temp_category'] = pd.cut(
    bs_hours_df['atemp'], bins=bins, labels=labels, include_lowest=True)
temp_grouped = bs_hours_df.groupby('temp_category', observed=True)[
    'count'].mean().reset_index()

# Dashboard Streamlit
st.subheader(
    ' Sejauh mana suhu memengaruhi pilihan seseorang untuk bersepeda?')

# Visualisasi Data
st.subheader("Rata-rata Penggunaan Sepeda Berdasarkan Kategori Suhu")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='temp_category',
    y='count',
    hue='temp_category',
    data=temp_grouped,
    palette='coolwarm',
    legend=False,
    edgecolor='black',
    ax=ax
)

for index, value in enumerate(temp_grouped['count']):
    ax.text(index, value + 5, f'{value:.2f}',
            ha='center', fontsize=10, fontweight='bold')

ax.set_title('Rata-rata Penggunaan Sepeda Berdasarkan Kategori Suhu 🌡️',
             fontsize=16, fontweight='bold', fontname='Segoe UI Emoji')
ax.set_xlabel('Kategori Suhu', fontsize=12, fontname='Segoe UI Emoji')
ax.set_ylabel('Rata-rata Penggunaan Sepeda',
              fontsize=12, fontname='Segoe UI Emoji')
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.tick_params(axis='x', labelsize=11)
ax.tick_params(axis='y', labelsize=11)

st.pyplot(fig)
