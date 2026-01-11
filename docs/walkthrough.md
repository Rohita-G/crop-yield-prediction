# Crop Yield Model Walkthrough

## Overview
We successfully built a machine learning pipeline to predict **Corn Yield** in the US Corn Belt using historical weather and soil data.

## 1. Data Processing
- **Source**: [Khaki et al. Dataset](https://huggingface.co/datasets/notadib/usa-corn-belt-crop-yield)
- **Features**: ~400 columns including weekly weather data (Precipitation, Temperature, etc.) and soil properties.
- **Samples**: 25,306 total.
- **Split**: Trained on data pre-2018 (24,835 samples), Tested on 2018 (471 samples).

## 2. Model Performance
We trained a **Random Forest Regressor** (n_estimators=50).

| Metric | Value | Meaning |
|---|---|---|
| **MAE** | **24.50** | On average, predictions are off by ~24.5 Bu/Acre. |
| **RMSE** | **30.08** | Root Mean Square Error. |
| **R² Score** | **0.31** | The model explains 31% of the variance in yield. |

> [!NOTE]
> An R² of 0.31 indicates that weather and static soil features alone capture some signal, but other factors (seed variety, pests, management practices) are likely significant drivers not present in this dataset.

## 3. Visualizations

### Actual vs Predicted Yield (2018)
![Actual vs Predicted](/Users/rohita/Environmental Sensing and Crop Yield Modeling Using Weather and Agricultural Data/results/predictions_vs_actual.png)
*Points closer to the red dashed line indicate better predictions.*

### Feature Importance
![Feature Importance](/Users/rohita/Environmental Sensing and Crop Yield Modeling Using Weather and Agricultural Data/results/feature_importance.png)
*Top factors driving the model's predictions.*

### Yield Distribution
![Yield Distribution](/Users/rohita/Environmental Sensing and Crop Yield Modeling Using Weather and Agricultural Data/results/corn_yield_distribution.png)
*Distribution of Corn Yield in the dataset.*

## 4. Next Steps to Improve
1.  **Hyperparameter Tuning**: Optimize the Random Forest.
2.  **Deep Learning**: Implement LSTM/CNN for better time-series pattern recognition (as suggested by the dataset authors).
3.  **Feature selection**: Remove noise from 400+ features.
