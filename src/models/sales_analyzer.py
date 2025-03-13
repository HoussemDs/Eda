import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from typing import Dict, Tuple

class SalesAnalyzer:
    @staticmethod
    def analyze_sales_trends(df: pd.DataFrame) -> Dict:
        """Analyze sales trends and patterns.
        
        Args:
            df (pd.DataFrame): Processed dataframe
            
        Returns:
            Dict: Dictionary containing sales trend analysis
        """
        analysis = {
            'total_sales': df['total_amount'].sum(),
            'avg_daily_sales': df.groupby('transaction_date')['total_amount'].sum().mean(),
            'peak_sales_hour': df.groupby('hour')['total_amount'].sum().idxmax(),
            'best_performing_category': df.groupby('product_category')['total_amount'].sum().idxmax(),
            'best_performing_store': df.groupby('store_location')['total_amount'].sum().idxmax(),
            'sales_growth': SalesAnalyzer._calculate_sales_growth(df)
        }
        return analysis
    
    @staticmethod
    def analyze_product_performance(df: pd.DataFrame) -> pd.DataFrame:
        """Analyze product performance metrics.
        
        Args:
            df (pd.DataFrame): Processed dataframe
            
        Returns:
            pd.DataFrame: Product performance metrics
        """
        product_metrics = df.groupby(['product_category', 'product_type']).agg({
            'transaction_qty': 'sum',
            'total_amount': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        
        product_metrics['avg_price'] = product_metrics['total_amount'] / product_metrics['transaction_qty']
        product_metrics['sales_share'] = product_metrics['total_amount'] / product_metrics['total_amount'].sum()
        
        return product_metrics.sort_values('total_amount', ascending=False)
    
    @staticmethod
    def analyze_store_performance(df: pd.DataFrame) -> pd.DataFrame:
        """Analyze store performance metrics.
        
        Args:
            df (pd.DataFrame): Processed dataframe
            
        Returns:
            pd.DataFrame: Store performance metrics
        """
        store_metrics = df.groupby(['store_id', 'store_location']).agg({
            'transaction_id': 'count',
            'total_amount': 'sum',
            'transaction_qty': 'sum'
        }).reset_index()
        
        store_metrics['avg_transaction_value'] = store_metrics['total_amount'] / store_metrics['transaction_id']
        store_metrics['sales_share'] = store_metrics['total_amount'] / store_metrics['total_amount'].sum()
        
        return store_metrics.sort_values('total_amount', ascending=False)
    
    @staticmethod
    def segment_customers(df: pd.DataFrame, n_clusters: int = 3) -> Tuple[pd.DataFrame, KMeans]:
        """Segment customers based on their purchasing behavior.
        
        Args:
            df (pd.DataFrame): Processed dataframe
            n_clusters (int): Number of clusters for segmentation
            
        Returns:
            Tuple[pd.DataFrame, KMeans]: Segmentation results and model
        """
        # Create customer features
        customer_features = df.groupby('transaction_id').agg({
            'total_amount': 'sum',
            'transaction_qty': 'sum',
            'product_id': 'nunique'
        }).reset_index()
        
        # Normalize features
        features_normalized = (customer_features.drop('transaction_id', axis=1) - 
                             customer_features.drop('transaction_id', axis=1).mean()) / \
                             customer_features.drop('transaction_id', axis=1).std()
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        customer_features['segment'] = kmeans.fit_predict(features_normalized)
        
        return customer_features, kmeans
    
    @staticmethod
    def _calculate_sales_growth(df: pd.DataFrame) -> float:
        """Calculate sales growth rate.
        
        Args:
            df (pd.DataFrame): Processed dataframe
            
        Returns:
            float: Sales growth rate
        """
        monthly_sales = df.groupby(df['datetime'].dt.to_period('M'))['total_amount'].sum()
        if len(monthly_sales) > 1:
            growth_rate = (monthly_sales.iloc[-1] - monthly_sales.iloc[0]) / monthly_sales.iloc[0] * 100
            return growth_rate
        return 0.0
