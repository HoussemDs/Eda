import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from src.data.data_loader import DataLoader
from src.preprocessing.preprocessor import DataPreprocessor
from src.features.feature_engineering import FeatureEngineer
from src.visualization.sales_visualizer import SalesVisualizer
from src.models.sales_analyzer import SalesAnalyzer

def main():
    print("Starting Coffee Shop Sales Analysis...")
    
    # Initialize components
    loader = DataLoader('Coffee Shop Sales.xlsx')
    preprocessor = DataPreprocessor()
    feature_engineer = FeatureEngineer()
    visualizer = SalesVisualizer('reports/figures')
    analyzer = SalesAnalyzer()
    
    # Load and process data
    print("\n1. Loading data...")
    df = loader.load_data()
    
    print("\n2. Preprocessing data...")
    df_processed = preprocessor.preprocess_data(df)
    quality_metrics = preprocessor.check_data_quality(df_processed)
    print("\nData Quality Metrics:")
    for metric, value in quality_metrics.items():
        print(f"{metric}: {value}")
    
    print("\n3. Engineering features...")
    df_featured = (df_processed
                  .pipe(feature_engineer.create_time_features)
                  .pipe(feature_engineer.create_sales_features)
                  .pipe(feature_engineer.create_store_features))
    
    print("\n4. Analyzing sales trends...")
    sales_trends = analyzer.analyze_sales_trends(df_featured)
    print("\nSales Trend Analysis:")
    for metric, value in sales_trends.items():
        print(f"{metric}: {value}")
    
    print("\n5. Analyzing product performance...")
    product_metrics = analyzer.analyze_product_performance(df_featured)
    print("\nTop 5 Products by Sales:")
    print(product_metrics.head())
    
    print("\n6. Analyzing store performance...")
    store_metrics = analyzer.analyze_store_performance(df_featured)
    print("\nStore Performance:")
    print(store_metrics)
    
    print("\n7. Creating visualizations...")
    visualizer.plot_daily_sales_trend(df_featured)
    visualizer.plot_hourly_sales_pattern(df_featured)
    visualizer.plot_product_category_sales(df_featured)
    visualizer.plot_store_performance(df_featured)
    visualizer.plot_sales_heatmap(df_featured)
    
    print("\n8. Performing customer segmentation...")
    customer_segments, model = analyzer.segment_customers(df_featured)
    print("\nCustomer Segments Summary:")
    print(customer_segments.groupby('segment').agg({
        'total_amount': ['mean', 'count'],
        'transaction_qty': 'mean',
        'product_id': 'mean'
    }).round(2))
    
    print("\nAnalysis complete! Check the 'reports/figures' directory for visualizations.")

if __name__ == "__main__":
    main()
