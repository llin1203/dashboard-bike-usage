import streamlit as st
import pandas as pd
import plotly.express as px

# Load_Datasets
day_data = pd.read_csv("https://raw.githubusercontent.com/llin1203/dashboard-bike-usage/refs/heads/main/dashboard/day_wrangled.csv")
hour_data = pd.read_csv("https://raw.githubusercontent.com/llin1203/dashboard-bike-usage/refs/heads/main/dashboard/hour_wrangled.csv")

st.title("BIKE USAGE DATA DASHBOARD")

# Dashboard_Description
st.markdown("""
    **Bike Usage Data** menampilkan informasi terkait jumlah penggunaan sepeda berdasarkan hari dan jam. 
    Dashboard ini dibuat untuk menjawab beberapa pertanyaan bisnis (case) terkait pola penggunaan sepeda.
""")

# Pilih_dataset
dataset_option = st.selectbox("Pilih Dataset:", ["Daily Usage", "Hourly Usage"])
data = day_data if dataset_option == "Daily Usage" else hour_data

# Pilih_Case
business_question = st.selectbox("Pilih Case", [
    "Peningkatan Penggunaan Sepeda berdasarkan Musim (Pertanyaan 1)",
    "Perubahan Tren Penggunaan Sepeda dari tahun 2011-2012 (Pertanyaan 2)",
    "Hubungan Cuaca dan Musim terhadap Penggunaan Sepeda (Pendukung Pertanyaan 1)",
    "Hubungan Cuaca dan Tahun terhadap Penggunaan Sepeda (Pendukung Pertanyaan 2)"
    
])

# Filter_tanggal
min_date = pd.to_datetime("2011-01-01")
max_date = pd.to_datetime("2012-12-31")

start_date = st.date_input("Pilih Tanggal Awal", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("Pilih Tanggal Akhir", min_value=min_date, max_value=max_date, value=max_date)

if start_date > end_date:
    st.error("Tanggal awal tidak boleh lebih besar daripada tanggal akhir! Silakan pilih ulang.")
elif start_date == end_date:
    st.warning("Harap pilih rentang tanggal minimal 2 tanggal agar data valid.")

data = data[(pd.to_datetime(data["dteday"]) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(data["dteday"]) <= pd.to_datetime(end_date))]

data["cnt"] = data["cnt"].astype(int)

# Mapping_season-weather
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_mapping = {1: "Clear", 2: "Mist", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}

# Fungsi_normalisasi
def normalize_values(df, column):
    min_val = df[column].min()
    max_val = df[column].max()
    if min_val == max_val:
        df[column] = 3  
    else:
        df[column] = ((df[column] - min_val) / (max_val - min_val) * 4 + 1).astype(int)
    return df

# Visualisasi_data
if business_question == "Peningkatan Penggunaan Sepeda berdasarkan Musim (Pertanyaan 1)":
    season_data = data.groupby("season").agg({"cnt": "sum"}).reset_index()
    season_data["season"] = season_data["season"].map(season_mapping)
    season_data = normalize_values(season_data, "cnt")

    fig = px.bar(season_data, x="season", y="cnt", 
                 labels={"cnt": "Bike-Usage", "season": "Season"},
                 title="Bike Usage by Season",
                 color_discrete_sequence=["green", "yellow", "orange", "blue"])

    st.plotly_chart(fig, use_container_width=True)
    
    # Kesimpulan
    st.markdown("Kesimpulan:")
    st.markdown("""
    - Musim dengan penggunaan sepeda tertinggi: Pada Fall (Musim Gugur) dan Summer (Musim Panas).
    - Cuaca mendukung **(lihat case hubungan cuaca dengan musim)** dan jam siang lebih panjang.
    - Musim dengan penggunaan terendah: Pada Winter (Musim Dingin) karena kondisi tidak mendukung.
    """)

elif business_question == "Perubahan Tren Penggunaan Sepeda dari tahun 2011-2012 (Pertanyaan 2)":
    year_data = data.groupby("yr").agg({"cnt": "sum"}).reset_index()
    year_data["yr"] = year_data["yr"].replace({0: "2011", 1: "2012"})
    year_data = normalize_values(year_data, "cnt")

    fig = px.bar(year_data, x=year_data["yr"].astype(str), y="cnt",
             labels={"cnt": "Bike-Usage", "yr": "Year"},
             title="Bike-Usage by Year (2011 vs 2012)",
             color_discrete_sequence=["yellow", "red"])

    fig.update_xaxes(title = "Year", type='category')
    st.plotly_chart(fig, use_container_width=True)
    
    # Kesimpulan
    st.markdown("Kesimpulan:")
    st.markdown("""
    - Tren penggunaan sepeda mengalami perubahan dari 2011 ke 2012, terlihat dalam grafik meningkatnya pengunaan sepeda ditahun 2012.
    - Cuaca lebih mendukung **(lihat case hubungan tahun dengan cuaca)** dibandingkan tahun sebelumnya.
    """)

elif business_question == "Hubungan Cuaca dan Tahun terhadap Penggunaan Sepeda (Pendukung Pertanyaan 2)":
    weather_year_data = data.groupby(["yr", "weathersit"]).agg({"cnt": "sum"}).reset_index()
    weather_year_data["yr"] = weather_year_data["yr"].replace({0: "2011", 1: "2012"})
    weather_year_data["weathersit"] = weather_year_data["weathersit"].map(weather_mapping)
    weather_year_data = normalize_values(weather_year_data, "cnt")

    fig = px.bar(weather_year_data, x="yr", y="cnt", color="weathersit",
                 labels={"cnt": "Bike-Usage", "yr": "Year", "weathersit": "Weather Condition"},
                 title="Bike Usage by Weather and Year",
                 barmode="group")

    st.plotly_chart(fig, use_container_width=True)
    
    # Kesimpulan
    st.markdown("Kesimpulan:")
    st.markdown("""
    - Tahun 2012 lebih tinggi dibanding 2011 karena lebih banyak hari cerah(clear).
    - Penggunaan sepeda paling tinggi saat cuaca cerah(clear).
    - Penggunaan menurun saat hujan atau salju.
    
    """)

elif business_question == "Hubungan Cuaca dan Musim terhadap Penggunaan Sepeda (Pendukung Pertanyaan 1)":
    weather_season_data = data.groupby(["season", "weathersit"]).agg({"cnt": "sum"}).reset_index()
    weather_season_data["season"] = weather_season_data["season"].map(season_mapping)
    weather_season_data["weathersit"] = weather_season_data["weathersit"].map(weather_mapping)
    weather_season_data = normalize_values(weather_season_data, "cnt")

    fig = px.bar(weather_season_data, x="season", y="cnt", color="weathersit",
                 labels={"cnt": "Bike-Usage", "season": "Season", "weathersit": "Weather Condition"},
                 title="Bike Usage by Weather and Season",
                 barmode="group")

    st.plotly_chart(fig, use_container_width=True)
    
    # Kesimpulan
    st.markdown("Kesimpulan:")
    st.markdown("""
    - Cuaca cerah dan musim panas meningkatkan penggunaan sepeda.
    - Musim dingin dan hujan/salju menurunkan penggunaan drastis.
    """)
