# Data Dictionary

## Dataset Source
**Repository**: [Hugging Face: notadib/usa-corn-belt-crop-yield](https://huggingface.co/datasets/notadib/usa-corn-belt-crop-yield)
**Original Authors**: Khaki et al. (2020), processed by Hasan et al. (2026).
**Filename**: `data/raw/khaki_multi_crop_yield.csv`

## Overview
The dataset contains historical crop yield, weather, and soil data for 763 counties in the US Corn Belt from 1980 to 2018.

## Column Definitions

### 1. Identifiers & Location
| Column | Description |
|---|---|
| `State` | US State name (e.g., Illinois) |
| `County` | US County name |
| `year` | Year of observation (1980-2018) |
| `lat` | Latitude of the county centroid |
| `lng` | Longitude of the county centroid |
| `loc_ID` | Unique location identifier |

### 2. Targets (Crop Yields)
Yield values are typically in **Bushels per Acre (Bu/Acre)**.
| Column | Description |
|---|---|
| `corn_yield` | Yield of Corn |
| `soybean_yield` | Yield of Soybean |
| `winter_wheat_yield` | Yield of Winter Wheat |

### 3. Weather Variables (`W_i_j`)
Weather data is aggregated weekly (52 weeks per year).
Format: `W_[Variable_Index]_[Week]`
- `i` (Variable Index):
    - `1`: Precipitation
    - `2`: Solar Radiation
    - `3`: Snow Water Equivalent
    - `4`: Max Temperature
    - `5`: Min Temperature
    - `6`: Vapor Pressure
- `j` (Week): 1 to 52

*Example*: `W_4_26` = Max Temperature for Week 26.

### 4. Soil Properties
Soil measurements at various depths (`0-5cm`, `5-15cm`, `15-30cm`, `30-60cm`, `60-100cm`, `100-200cm`).
- `bdod`: Bulk Density
- `cec`: Cation Exchange Capacity
- `cfvo`: Volumetric Fraction of Coarse Fragments
- `clay`: Clay content
- `nitrogen`: Nitrogen content
- `ocd`: Organic Carbon Density
- `ocs`: Organic Carbon Stocks
- `phh2o`: pH in water
- `sand`: Sand content
- `silt`: Silt content
- `soc`: Soil Organic Carbon

*Example*: `nitrogen_mean_0-5cm` = Mean Nitrogen content at 0-5cm depth.

### 5. Other
- `P_1` to `P_14`: Preprocessed features or agricultural practice indicators (precise definitions pending, likely planting windows or fertilizer usage proxies).
