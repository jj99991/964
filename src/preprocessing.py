import pandas as pd
import numpy as np


def load_and_preprocess_data(file_path="data/salesdaily.csv"):
    """Loads raw transactional history, aggregates it to a weekly grain to smooth
    chaotic noise, engineers historical lags, and applies cyclical encoding."""
    df = pd.read_csv(file_path)

    # 1. Convert the string date column into a proper Datetime Index
    df['datum'] = pd.to_datetime(df['datum'])
    df = df.set_index('datum')

    # 2. AGGREGATE TO WEEKLY GRAIN: Smooth out day-to-day random spikes
    atc_categories = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

    # Sum the drug volumes per week, and grab the first calendar values for metadata
    df_weekly = df[atc_categories].resample('W').sum()
    df_meta = df[['Year', 'Month', 'Weekday Name']].resample('W').first()

    # Recombine into a unified weekly dataset
    df = pd.concat([df_meta, df_weekly], axis=1).reset_index()

    # 3. Generate 1-week and 2-week historical lags per drug class independently
    for drug in atc_categories:
        df[f'{drug}_Lag_1'] = df[drug].shift(1)
        df[f'{drug}_Lag_2'] = df[drug].shift(2)

    # Drop rows containing empty shifts
    df = df.dropna().reset_index(drop=True)

    # 4. Cyclical Month Encoding
    df['Month_Sin'] = np.sin(2 * np.pi * df['Month'] / 12.0)
    df['Month_Cos'] = np.cos(2 * np.pi * df['Month'] / 12.0)

    # 5. Feature Reduction: Drop operational metadata and the timestamp column
    # FIX: Adding 'datum' here prevents it from leaking into the training matrices!
    df = df.drop(columns=['datum', 'Hour'], errors='ignore')

    # 6. Categorical Vectorization for the Weekday column
    df_encoded = pd.get_dummies(df, columns=['Weekday Name'], drop_first=True)

    # Strict float casting for boolean dummy vectors
    bool_cols = df_encoded.select_dtypes(include=['bool']).columns
    df_encoded[bool_cols] = df_encoded[bool_cols].astype(float)

    return df_encoded