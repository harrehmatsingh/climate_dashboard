import streamlit as st
import pandas as pd

df = pd.read_csv("data/cleaned/climate_cleaned.csv")
df["date"] = pd.to_datetime(df["date"])

# Extract month
month = df["date"].dt.month

# Create season column
df["season"] = pd.Series(pd.NA, index=df.index)

#setting up seasons
df.loc[month.isin([12, 1, 2]), "season"] = "Winter"
df.loc[month.isin([3, 4, 5]), "season"] = "Spring"
df.loc[month.isin([6, 7, 8]), "season"] = "Summer"
df.loc[month.isin([9, 10, 11]), "season"] = "Fall"

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
        index=1  
    )
    
    st.subheader("Season Filter")
    season = st.multiselect(
        "Select season(s)",
        ["Winter", "Spring", "Summer", "Fall"],
        default=["Winter", "Spring", "Summer", "Fall"]
    )
    
    
    st.subheader("Comparison Mode")
    comparison_mode = st.radio(
        "Switch comparison mode:",
        ["On", "Off"]
    )
    
    
# trim the actual df to selected preferences
sub_df = df[df["date"].between(start_date, end_date)] # trim teh df to selected time frame

# get only the selected seasons
if season:
    sub_df = sub_df.loc[sub_df["season"].isin(season)]
    
# group the sub df by selected aggregation
if aggregation == "Daily":
    grouped_dfs = {"Daily": sub_df.copy()}
        
elif aggregation == "Monthly":
    grouped_dfs = {
        key: group.copy()
        for key, group in sub_df.groupby([sub_df["date"].dt.year, sub_df["date"].dt.month])
    }
    
elif aggregation == "Seasonal":
    grouped_dfs = {
        key: group.copy()
        for key, group in sub_df.groupby([sub_df["date"].dt.year, sub_df["season"]])
    }
    
elif aggregation == "Annual":
    grouped_dfs = {
        key: group.copy()
        for key, group in sub_df.groupby(sub_df["date"].dt.year)
    }
    
    

