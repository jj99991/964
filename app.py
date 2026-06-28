import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.preprocessing import load_and_preprocess_data
from src.model_trainer import train_drug_forecast_model

# 1. UI Window Layout Instantiation
st.set_page_config(page_title="PrescriptionForecast", layout="wide")
st.title("Prescription Forecast: Pharmaceutical Demand Planner")
st.markdown("---")

# 2. Pipeline Initialization
df_processed = load_and_preprocess_data()
atc_list = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

# 3. Sidebar Parameter Controls
st.sidebar.header("Predictive Scope Settings")
selected_atc = st.sidebar.selectbox("Select Target Drug Class (ATC):", atc_list, index=3)

# Dynamic retraining in background based on target selection
model, feature_names, mse, r2, y_test, y_pred = train_drug_forecast_model(df_processed, selected_atc)

st.sidebar.markdown("### 🗓️ Future Forecasting Horizon")
input_year = st.sidebar.slider("Target Year Selection:", 2024, 2030, 2026)
input_month = st.sidebar.slider("Target Month Selection:", 1, 12, 6)

# 4. Integrated Inference Logic
input_encoded = {
    'Year': input_year,
    'Month': input_month,
    'Month_Sin': np.sin(2 * np.pi * input_month / 12.0),
    'Month_Cos': np.cos(2 * np.pi * input_month / 12.0),
}

# Automatically bind the remaining features (lags and encoded flags) from the last known state
for col in feature_names:
    if col not in input_encoded:
        input_encoded[col] = df_processed[col].iloc[-1]

# Sort the feature keys exactly as expected by the trained scikit-learn model
inference_df = pd.DataFrame([input_encoded])[feature_names]
prediction = max(0.0, model.predict(inference_df)[0])

# 5. Output Display
st.subheader("Optimization & Inventory Forecasting Outputs")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=f"Predicted Weekly Demand Volume ({selected_atc})", value=f"{prediction:.2f} Units")
with col2:
    st.metric(label="Goodness of Fit ($R^2$ Score)", value=f"{r2:.4f}")
with col3:
    st.metric(label="Mean Squared Error (MSE)", value=f"{mse:.4f}")

st.markdown("---")

# 6. Visualization Views Embedding
st.subheader("Diagnostic Visualizations Dashboard")
tab1, tab2, tab3 = st.tabs(["Longitudinal Trends", "Category Sales Distribution", "Model Convergence Fit"])

with tab1:  # Chart 1: Line Chart (Updated to read from the unified dataset)
    st.markdown("#### Historical Sales Volatility Time-Series Trend Line")
    fig1, ax1 = plt.subplots(figsize=(8, 3))

    # Aggregate processed weekly rows into timeline groups for smooth display
    monthly_trends = df_processed.groupby(['Year', 'Month'])[selected_atc].sum().reset_index()
    monthly_trends['Timeline'] = monthly_trends['Year'].astype(int).astype(str) + "-" + monthly_trends['Month'].astype(
        int).astype(str).str.zfill(2)

    sns.lineplot(data=monthly_trends, x='Timeline', y=selected_atc, ax=ax1, color="darkblue", marker="o")

    # 1:1 Clean Axis Slicing
    tick_spacing = 4
    ticks = list(range(0, len(monthly_trends['Timeline']), tick_spacing))
    labels = [monthly_trends['Timeline'].iloc[i] for i in ticks]
    ax1.set_xticks(ticks)
    ax1.set_xticklabels(labels, rotation=45, fontsize=8, ha='right')

    ax1.set_xlabel("Historical Baseline Timeline (YYYY-MM)")
    ax1.set_ylabel("Aggregated Quantities Sold")
    st.pyplot(fig1, use_container_width=False)

with tab2:  # Chart 2: Bar Chart
    st.markdown("#### Cumulative Product Volume Across All 8 ATC Classifications")
    fig2, ax2 = plt.subplots(figsize=(7, 3))
    sales_sums = df_processed[atc_list].sum()
    sns.barplot(x=sales_sums.index, y=sales_sums.values, ax=ax2, palette="muted")
    ax2.set_xlabel("ATC Classification Code labels")
    ax2.set_ylabel("Total Unit Distributions Volume")
    st.pyplot(fig2, use_container_width=False)

with tab3:  # Chart 3: Scatterplot
    st.markdown("#### Predicted vs. Actual Convergence Line (Supervised Accuracy Diagnostic)")
    fig3, ax3 = plt.subplots(figsize=(5.5, 3.5))
    ax3.scatter(y_test, y_pred, color="black", alpha=0.5, label="Test Observations")
    limits = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax3.plot(limits, limits, color="crimson", linewidth=2.5, label="Perfect Model Calibration ($Y = \hat{Y}$)")
    ax3.set_xlabel("Empirical Real Weekly Sales Targets ($Y_{test}$)")
    ax3.set_ylabel("Algorithm Predicted Weekly Value ($\hat{Y}_{pred}$)")
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    st.pyplot(fig3, use_container_width=False)
