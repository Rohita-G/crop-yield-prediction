import pytest
import numpy as np
import os
from src.model import CropYieldModel
from src.config import config

def test_model_initialization():
    model = CropYieldModel(n_estimators=10)
    assert model.n_estimators == 10
    
def test_model_training_mock_data():
    # Mock efficient data
    X_train = np.random.rand(100, 5)
    y_train = np.random.rand(100) * 100
    
    model = CropYieldModel(n_estimators=5)
    model.train(X_train, y_train)
    
    # Verify predict runs
    X_test = np.random.rand(10, 5)
    preds = model.model.predict(X_test)
    assert len(preds) == 10
    
def test_model_saving(tmp_path):
    # Train
    X = np.random.rand(10, 2)
    y = np.random.rand(10)
    model = CropYieldModel(n_estimators=1)
    model.train(X, y)
    
    # Save
    save_path = tmp_path / "model.pkl"
    model.save(str(save_path))
    assert os.path.exists(save_path)
