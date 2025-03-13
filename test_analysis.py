import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from src.data.data_loader import DataLoader
from src.preprocessing.preprocessor import DataPreprocessor
from src.models.sales_analyzer import SalesAnalyzer

def main():
    print("Starting Basic Analysis Test...")
    
    # 1. Load Data
    print("\n1. Loading data...")
    loader = DataLoader('Coffee Shop Sales.xlsx')
    df = loader.load_data()
    print(f"Initial data shape: {df.shape}")
    
    # 2. Basic data info
    print("\n2. Data Info:")
    print("\nColumns:", df.columns.tolist())
    print("\nSample data:")
    print(df.head())
    
    # 3. Preprocess
    print("\n3. Preprocessing data...")
    preprocessor = DataPreprocessor()
    df_processed = preprocessor.preprocess_data(df)
    
    print("\nProcessed data columns:", df_processed.columns.tolist())
    print("\nSample processed data:")
    print(df_processed.head())
    
    # 4. Basic Analysis
    print("\n4. Basic Analysis...")
    analyzer = SalesAnalyzer()
    sales_trends = analyzer.analyze_sales_trends(df_processed)
    
    print("\nSales Trends:")
    for metric, value in sales_trends.items():
        print(f"{metric}: {value}")

if __name__ == "__main__":
    main()
