import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = Path("data/raw/climate_raw.csv")
PROCESSED_PATH = Path("data/cleaned/climate_cleaned.csv")


def clean_data(path):
    
    df = pd.read_csv(path)
    
    #we want last 25 years' data (2001 to 2025)
    df = df.iloc[1:] #remove the first row = Jan 1, 2026
    df = df.head(9131) # 9131 days from 31st Dec, 2025 to 1st Jan, 2001
    
    df = df.loc[:, ["date", "max_temperature", "avg_temperature", "min_temperature", "avg_relative_humidity", "avg_dew_point", "avg_wind_speed", "avg_pressure_sea", "avg_visibility", "min_visibility", 
                    "avg_health_index", "precipitation", "daylight", "solar_radiation", "avg_cloud_cover_8", "heatdegdays", "cooldegdays", "growdegdays_7" ]]
    
    return df

def main():

    print("Cleaning data...")
    df_clean = clean_data(RAW_PATH)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_PATH, index=False)

    print(f"Cleaned data saved to {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
    