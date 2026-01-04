import streamlit as st
import pandas as pd

df = pd.read_csv("data/cleaned/climate_cleaned.csv")
df["date"] = pd.to_datetime(df["date"])

st.title("Climate Dashboard")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

# date range slider
date_range = st.slider(
    "Select date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)

start_date, end_date = date_range  
