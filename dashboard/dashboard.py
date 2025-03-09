import pandas as pd
import plotly.express as px
import streamlit as st
import os


# Main_data yang merupakan hasil dari data wrangling
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "main_data.csv")
    return pd.read_csv(csv_path)


main_data = load_data()

# Streamlit layout
st.title("Bike Usage Data")

# Dropdown untuk memilih kategori visualisasi
category = st.selectbox(
    "Select Category", ["season", "weathersit", "hr", "weekday", "mnth"], index=0
)

# Dropdown untuk memilih tipe plot
plot_type = st.selectbox("Select Plot Type", ["Bar Chart", "Line Chart"], index=0)

# Kelompokkan data berdasarkan kategori yang dipilih
grouped_df = main_data.groupby(category).agg({"cnt": "sum"}).reset_index()

# Buat grafik sesuai dengan tipe plot yang dipilih
if plot_type == "Bar Chart":
    fig = px.bar(
        grouped_df,
        x=category,
        y="cnt",
        labels={"cnt": "Total Bike Rentals", category: category.capitalize()},
        title=f"Total Bike Rentals by {category.capitalize()}",
    )
else:
    fig = px.line(
        grouped_df,
        x=category,
        y="cnt",
        labels={"cnt": "Total Bike Rentals", category: category.capitalize()},
        title=f"Total Bike Rentals by {category.capitalize()}",
    )

# Tampilkan grafik di Streamlit
st.plotly_chart(fig)
