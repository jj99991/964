from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def train_drug_forecast_model(df_preprocessed, target_atc_category):
    """Executes a deterministic 80/20 matrix split and fits a Multiple Linear
    Regression model using ONLY the target drug's specific history to prevent cross-leakage."""

    # 1. Core target columns representing current sales
    atc_categories = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

    # 2. Identify and drop lag features belonging to ALL OTHER drugs
    other_drugs = [drug for drug in atc_categories if drug != target_atc_category]
    lag_cols_to_drop = [col for col in df_preprocessed.columns if any(col.startswith(d + '_Lag_') for d in other_drugs)]

    # 3. Cleanly isolate independent features matrix X
    # Drops current sales for all drugs AND foreign lag features
    X = df_preprocessed.drop(columns=atc_categories + lag_cols_to_drop)
    y = df_preprocessed[target_atc_category]

    # Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    # Instantiate and fit supervised model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate testing performance matrices
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return model, X.columns.tolist(), mse, r2, y_test, y_pred