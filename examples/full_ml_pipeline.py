"""
Complete Machine Learning Pipeline Example

This script demonstrates a complete end-to-end ML pipeline:
1. Data collection
2. Feature engineering
3. Train/test split
4. Model training
5. Evaluation
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

from tradingview_screener import Query, col
from tradingview_screener.ml_collector import MLDataCollector
from tradingview_screener.features import (
    add_returns,
    add_price_momentum,
    add_volume_features,
    add_volatility,
    add_technical_flags,
    create_target_variable,
    handle_missing_values,
    remove_outliers,
)

print("="*70)
print("COMPLETE ML PIPELINE: Stock Price Direction Prediction")
print("="*70)

# Step 1: Data Collection
print("\n[1/5] Collecting market data...")
collector = MLDataCollector(
    output_dir='data/ml_pipeline',
    format='parquet',
)

query = (
    Query()
    .select(
        'name',
        'close',
        'open',
        'high',
        'low',
        'volume',
        'market_cap_basic',
        'relative_volume_10d_calc',
        'RSI',
        'MACD.macd',
        'MACD.signal',
        'EMA5',
        'EMA20',
        'EMA50',
        'EMA200',
        'change',
    )
    .where(
        col('market_cap_basic') > 5_000_000_000,
        col('volume') > 500_000,
    )
    .order_by('volume', ascending=False)
    .limit(1000)
)

df = collector.collect_once(query, dataset_name='training_data', save=True)
print(f"✓ Collected {len(df)} stocks")

# Step 2: Feature Engineering
print("\n[2/5] Engineering features...")

# Add technical features
df = add_returns(df, price_column='close', periods=[1, 5, 10, 20])
df = add_price_momentum(df, price_column='close', windows=[5, 10, 20, 50])
df = add_volume_features(df, volume_column='volume', windows=[5, 10, 20])
df = add_volatility(df, price_column='close', windows=[5, 10, 20])
df = add_technical_flags(df, price_column='close', volume_column='volume')

# Create target variable: predict if price goes up tomorrow
df = create_target_variable(
    df,
    price_column='close',
    target_type='direction',  # Binary classification
    periods=1,  # Predict 1 day ahead
    classification_threshold=0.0,
)

print(f"✓ Created {len(df.columns)} features")

# Step 3: Data Preprocessing
print("\n[3/5] Preprocessing data...")

# Handle missing values
df = handle_missing_values(df, strategy='median')

# Remove outliers
numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
numeric_cols = [c for c in numeric_cols if c != 'target']  # Don't remove target outliers
df = remove_outliers(df, columns=numeric_cols, method='iqr', threshold=1.5)

print(f"✓ Cleaned data shape: {df.shape}")

# Prepare features and target
feature_cols = [col for col in df.columns if col not in [
    'ticker', 'name', 'dataset_name', 'collection_timestamp',
    'collection_unix', 'target'
]]

X = df[feature_cols].select_dtypes(include=['number'])
y = df['target']

# Drop any remaining NaN values
valid_idx = ~(X.isnull().any(axis=1) | y.isnull())
X = X[valid_idx]
y = y[valid_idx]

print(f"✓ Final dataset: {len(X)} samples, {len(X.columns)} features")
print(f"✓ Target distribution: {y.value_counts().to_dict()}")

# Step 4: Train/Test Split and Model Training
print("\n[4/5] Training model...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest classifier
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)
print(f"✓ Model trained on {len(X_train)} samples")

# Step 5: Evaluation
print("\n[5/5] Evaluating model...")

# Predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_accuracy = (y_pred_train == y_train).mean()
test_accuracy = (y_pred_test == y_test).mean()

print(f"\nTrain Accuracy: {train_accuracy:.2%}")
print(f"Test Accuracy:  {test_accuracy:.2%}")

print("\nClassification Report (Test Set):")
print(classification_report(y_test, y_pred_test, target_names=['Down', 'Up']))

print("\nConfusion Matrix (Test Set):")
print(confusion_matrix(y_test, y_pred_test))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10).to_string(index=False))

# Save model and results
import pickle

model_path = 'data/ml_pipeline/trained_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

results_df = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
results_df.to_csv('data/ml_pipeline/feature_importance.csv', index=False)

print(f"\n✓ Model saved to: {model_path}")
print(f"✓ Feature importance saved to: data/ml_pipeline/feature_importance.csv")

print("\n" + "="*70)
print("ML PIPELINE COMPLETE!")
print("="*70)
print("\nNext steps:")
print("1. Fine-tune hyperparameters")
print("2. Try different models (XGBoost, LightGBM, Neural Networks)")
print("3. Deploy for real-time predictions")
print("4. Set up automated retraining with scheduled data collection")
