import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from .config import config
from .logger import get_logger

logger = get_logger(__name__)

class CropYieldModel:
    def __init__(self, n_estimators=None, random_state=None, n_jobs=None):
        self.n_estimators = n_estimators or config['model']['params']['n_estimators']
        self.random_state = random_state or config['model']['params']['random_state']
        self.n_jobs = n_jobs or config['model']['params']['n_jobs']
        
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            n_jobs=self.n_jobs
        )
        
    def train(self, X_train, y_train):
        logger.info(f"Training RandomForest(n_estimators={self.n_estimators})...")
        self.model.fit(X_train, y_train)
        logger.info("Training complete.")
        
    def evaluate(self, X_test, y_test):
        logger.info("Evaluating model...")
        predictions = self.model.predict(X_test)
        
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        r2 = r2_score(y_test, predictions)
        
        logger.info(f"MAE: {mae:.4f}")
        logger.info(f"RMSE: {rmse:.4f}")
        logger.info(f"R2 Score: {r2:.4f}")
        
        return predictions, {'mae': mae, 'rmse': rmse, 'r2': r2}
    
    def save(self, filepath=None):
        out_path = filepath or config['paths']['model_output']
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        joblib.dump(self.model, out_path)
        logger.info(f"Model saved to {out_path}")
        
    def plot_feature_importance(self, feature_names, save_path=None):
        out_path = save_path or os.path.join(config['paths']['plot_output'], 'feature_importance.png')
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        # Plot Top 20 Features
        top_n = 20
        plt.figure(figsize=(12, 8))
        plt.title("Top 20 Feature Importances")
        plt.bar(range(top_n), importances[indices[:top_n]], align="center")
        plt.xticks(range(top_n), [feature_names[i] for i in indices[:top_n]], rotation=90)
        plt.xlim([-1, top_n])
        plt.tight_layout()
        plt.savefig(out_path)
        logger.info(f"Feature importance plot saved to {out_path}")

if __name__ == "__main__":
    from .preprocessing import load_and_process_data
    
    # 1. Load Data
    X_train, X_test, y_train, y_test, scaler, feature_cols = load_and_process_data()
    
    # 2. Initialize and Train
    model = CropYieldModel()
    model.train(X_train, y_train)
    
    # 3. Evaluate
    preds, metrics = model.evaluate(X_test, y_test)
    
    # 4. Save Artifacts
    model.save()
    model.plot_feature_importance(feature_cols)
    
    # 5. Plot Predictions vs Actual
    plot_dir = config['paths']['plot_output']
    os.makedirs(plot_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, preds, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Yield')
    plt.ylabel('Predicted Yield')
    plt.title('Actual vs Predicted Corn Yield')
    plt.savefig(os.path.join(plot_dir, 'predictions_vs_actual.png'))
    logger.info(f"Prediction plot saved to {plot_dir}")
