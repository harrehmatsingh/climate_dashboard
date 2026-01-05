import streamlit as st
import pandas as pd

df = pd.read_csv("data/cleaned/climate_cleaned.csv")
df["date"] = pd.to_datetime(df["date"])

st.title("Climate Dashboard")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

with st.sidebar:
    
    st.header("Global Controls")
    
    st.subheader("Time Period")
    start_date, end_date = st.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    st.subheader("Aggregation Level")
    aggregation = st.selectbox(
        "Aggregate data by",
        ["Daily", "Monthly", "Seasonal", "Annual"],
        index=1  # Monthly default is sensible
    )
    
    st.subheader("Season Filter")
    season = st.multiselect(
        "Select season(s)",
        ["Winter", "Spring", "Summer", "Fall"],
        default=["Winter", "Spring", "Summer", "Fall"]
    )
    
    
    st.subheader("Comparison Mode")
    comparison_mode = st.radio(
        "Compare data by",
        ["Off", "Single Year", "Multiple Years", "Decade Comparison"]
    )

