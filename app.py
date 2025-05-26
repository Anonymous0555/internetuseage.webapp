import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page layout
st.set_page_config(page_title="Internet Usage Plotter", layout="wide")
st.title("📊 Internet Usage (% of Population)")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("1302f1f9-350a-413b-a954-2e4aa41aba2c.csv", skiprows=4)

df = load_data()

# Extract year columns (up to 2021 only)
year_columns = [col for col in df.columns if col.isdigit() and int(col) <= 2021]
years = list(map(int, year_columns))

# Input box
input_countries = st.text_input("Enter country names (comma-separated):", placeholder="e.g. India, Nigeria, Brazil")

if input_countries:
    countries = [c.strip().lower() for c in input_countries.split(",") if c.strip()]
    fig, ax = plt.subplots(figsize=(10, 5))
    has_data = False

    for country in countries:
        match = df[df["Country Name"].str.lower() == country]
        if match.empty:
            st.warning(f"No data for: {country.title()}")
            continue
        usage = match[year_columns].values.flatten().astype(float)
        ax.plot(years, usage, marker='o', label=match["Country Name"].values[0])
        has_data = True

    if has_data:
        ax.set_title("Internet Usage (% of Population)")
        ax.set_xlabel("Year")
        ax.set_ylabel("Users (%)")
        ax.set_ylim(0, 100)
        ax.grid(True)
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("No valid countries found.")
