import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from .config import config
from .logger import get_logger

logger = get_logger(__name__)

def run_eda():
    # Load data
    filepath = config['paths']['raw_data']
    logger.info(f"Loading data from {filepath}...")
    
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return

    # Basic Info
    # Using logger for info output is tricky as it formats it. 
    # For DataFrame info/head, we might convert to string and log it.
    import io
    buffer = io.StringIO()
    df.info(buf=buffer)
    logger.info(f"Data Info:\n{buffer.getvalue()}")
    
    logger.info(f"First 5 rows:\n{df.head()}")
    logger.info(f"Summary Statistics:\n{df.describe()}")
    
    # Check for missing values
    missing = df.isnull().sum().sort_values(ascending=False).head(10)
    logger.info(f"Missing Values:\n{missing}")
    
    # Plotting
    plot_dir = config['paths']['plot_output']
    os.makedirs(plot_dir, exist_ok=True)
    target_col = config['preprocessing']['target_col']
    
    if target_col in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[target_col].dropna(), kde=True)
        plt.title(f'{target_col} Distribution')
        plt.xlabel('Yield')
        plt.ylabel('Frequency')
        out_path = os.path.join(plot_dir, f'{target_col}_distribution.png')
        plt.savefig(out_path)
        logger.info(f"Saved {out_path}")
        
        # Plot Yield over Time (Average per year)
        plt.figure(figsize=(10, 6))
        df.groupby('year')[target_col].mean().plot()
        plt.title(f'Average {target_col} over Years')
        plt.xlabel('Year')
        plt.ylabel('Average Yield')
        plt.grid(True)
        out_path_time = os.path.join(plot_dir, f'{target_col}_over_time.png')
        plt.savefig(out_path_time)
        logger.info(f"Saved {out_path_time}")
        
    else:
        logger.warning(f"Column '{target_col}' not found.")

if __name__ == "__main__":
    run_eda()
