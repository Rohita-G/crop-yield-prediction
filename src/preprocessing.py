import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from .config import config
from .logger import get_logger

logger = get_logger(__name__)

def load_and_process_data(filepath=None, target_col=None):
    """
    Loads dataset, isolates Weather/Soil features, and splits into Train/Test.
    
    Args:
        filepath (str, optional): Path to CSV. Defaults to config.
        target_col (str, optional): Target column. Defaults to config.
        
    Returns:
        X_train, X_test, y_train, y_test, scaler
    """
    filepath = filepath or config['paths']['raw_data']
    target_col = target_col or config['preprocessing']['target_col']
    
    logger.info(f"Loading data from {filepath}...")
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise

    # 1. Drop Data with Missing Target
    initial_rows = len(df)
    df = df.dropna(subset=[target_col])
    dropped_rows = initial_rows - len(df)
    if dropped_rows > 0:
        logger.warning(f"Dropped {dropped_rows} rows with missing {target_col}")
    
    # 2. Define Features
    # Weather columns: W_1_1 to W_6_52
    weather_cols = [col for col in df.columns if col.startswith('W_')]
    
    # Soil columns: Named soil measurements (excluding P_)
    soil_keywords = ['bdod', 'cec', 'cfvo', 'clay', 'nitrogen', 'ocd', 'ocs', 'phh2o', 'sand', 'silt', 'soc']
    soil_cols = [col for col in df.columns if any(k in col for k in soil_keywords)]
    
    # Location/Year Features
    meta_cols = ['year', 'lat', 'lng']
    
    feature_cols = weather_cols + soil_cols + meta_cols
    
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    
    # 3. Handle Missing Values in Features (if any)
    X = X.fillna(0) # Simple imputation for now
    
    # 4. Train/Test Split (Time-based split preferred for time-series, but random for now as baseline)
    test_year = config['preprocessing']['test_year']
    mask_test = df['year'] == test_year
    mask_train = df['year'] < test_year
    
    X_train = X[mask_train]
    y_train = y[mask_train]
    X_test = X[mask_test]
    y_test = y[mask_test]
    
    logger.info(f"Training Samples (Pre-{test_year}): {X_train.shape[0]}")
    logger.info(f"Test Samples ({test_year}): {X_test.shape[0]}")
    
    # Save Processed Data for User Inspection
    logger.info("Saving processed data...")
    train_path = config['paths']['processed_train']
    test_path = config['paths']['processed_test']
    
    os.makedirs(os.path.dirname(train_path), exist_ok=True)
    
    # Recombine for saving (Unscaled features + Target)
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    logger.info(f"Saved {train_path} and {test_path}")

    # 5. Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_cols
