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
    
    start_date, end_date = st.slider(
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
    
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# trim the actual df to selected preferences
sub_df =df.loc[
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
] 

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
    
    
KPI_CONFIG = {
    "Mean Temperature": {
        "column": "avg_temperature",
        "agg": "mean",
        "unit": "°C",
        "format": "{:.1f}",
        "tooltip": "Average daily temperature over the selected period."
    },
    "Max Temperature": {
        "column": "max_temperature",
        "agg": "mean",
        "unit": "°C",
        "format": "{:.1f}",
        "tooltip": "Mean of daily maximum temperatures."
    },
    "Min Temperature": {
        "column": "min_temperature",
        "agg": "mean",
        "unit": "°C",
        "format": "{:.1f}",
        "tooltip": "Mean of daily minimum temperatures."
    },
    "Total Precipitation": {
        "column": "precipitation",
        "agg": "sum",
        "unit": "mm",
        "format": "{:.0f}",
        "tooltip": "Total accumulated precipitation."
    },
    "Cooling Degree Days": {
        "column": "cooldegdays",
        "agg": "sum",
        "unit": "",
        "format": "{:.0f}",
        "tooltip": "Indicator of cooling demand during warm periods."
    },
    "Heating Degree Days": {
        "column": "heatdegdays",
        "agg": "sum",
        "unit": "",
        "format": "{:.0f}",
        "tooltip": "Indicator of heating demand during cold periods."
    },
    "Growing Degree Days": {
        "column": "growdegdays_7",
        "agg": "sum",
        "unit": "",
        "format": "{:.0f}",
        "tooltip": "Indicator of plant growth potential."
    },
    "Solar Radiation": {
        "column": "solar_radiation",
        "agg": "mean",
        "unit": "W/m²",
        "format": "{:.0f}",
        "tooltip": "Average incoming solar energy."
    },
    "Health Index": {
        "column": "avg_health_index",
        "agg": "mean",
        "unit": "",
        "format": "{:.1f}",
        "tooltip": "Composite weather-related health index."
    }
}


def compute_kpi(df, column, agg):
    if df.empty:
        return None

    if agg == "mean":
        return df[column].mean()
    elif agg == "sum":
        return df[column].sum()
    elif agg == "max":
        return df[column].max()
    elif agg == "min":
        return df[column].min()
    else:
        raise ValueError(f"Unknown aggregation: {agg}")
    
    
def get_baseline_df(df, start_date, end_date, min_year=2001):
    """
    Creates a rolling baseline with the same duration as the selected range,
    shifted back by the same number of years.
    """

    # Compute duration in years (floor)
    n_years = max(end_date.year - start_date.year, 1)

    baseline_start = start_date.replace(year=start_date.year - (n_years + 1))
    baseline_end = end_date.replace(year=end_date.year - (n_years + 1))

    # Clamp to dataset minimum
    min_date = pd.Timestamp(f"{min_year}-01-01")
    
    if baseline_start < min_date:
        baseline_start = min_date

    baseline_df = df.loc[
        (df["date"] >= baseline_start) &
        (df["date"] <= baseline_end)
    ]
    
    return baseline_df


baseline_df = get_baseline_df(
    df=df,
    start_date=start_date,
    end_date=end_date,
    min_year=2001
)

st.subheader("Climate Overview")

cols = st.columns(4)
col_idx = 0

for kpi_name, cfg in KPI_CONFIG.items():

    current_value = compute_kpi(
        sub_df,
        cfg["column"],
        cfg["agg"]
    )

    baseline_value = compute_kpi(
        baseline_df,
        cfg["column"],
        cfg["agg"]
    )

    if current_value is None or baseline_value is None:
        delta = None
    else:
        delta = current_value - baseline_value

    formatted_value = (
        cfg["format"].format(current_value) + f" {cfg['unit']}"
        if current_value is not None
        else "N/A"
    )

    formatted_delta = (
        cfg["format"].format(delta)
        if delta is not None
        else None
    )

    with cols[col_idx]:
        st.metric(
            label=kpi_name,
            value=formatted_value,
            delta=formatted_delta,
            help=(
                f"{cfg['tooltip']} "
            )
        )
        
        baseline_df['date'] = pd.to_datetime(baseline_df['date'])
        base_start = baseline_df["date"].min()
        base_end = baseline_df["date"].max()
        
        if not pd.isna(base_start) and not pd.isna(base_end):
            st.caption(f"vs {base_start.year}-{base_end.year}")

    col_idx = (col_idx + 1) % 4


