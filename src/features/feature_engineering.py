import pandas as pd
import numpy as np
from typing import List

class FeatureEngineer:
    @staticmethod
    def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create time-based features for analysis.
        
        Args:
            df (pd.DataFrame): Input dataframe with datetime column
            
        Returns:
            pd.DataFrame: DataFrame with additional time features
        """
        df = df.copy()
        
        # Create cyclical features for hour
        df['hour_sin'] = np.sin(2 * np.pi * df['hour']/24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour']/24)
        
        # Create day of week numeric
        df['day_of_week_num'] = df['datetime'].dt.dayofweek
        
        # Is weekend feature
        df['is_weekend'] = df['day_of_week_num'].isin([5, 6]).astype(int)
        
        return df
    
    @staticmethod
    def create_sales_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create sales-related features.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: DataFrame with additional sales features
        """
        df = df.copy()
        
        # Calculate moving averages
        df['daily_sales'] = df.groupby('transaction_date')['total_amount'].transform('sum')
        df['daily_transactions'] = df.groupby('transaction_date')['transaction_id'].transform('count')
        
        # Calculate average transaction value
        df['avg_transaction_value'] = df['total_amount'] / df['transaction_qty']
        
        # Product popularity
        df['product_popularity'] = df.groupby('product_id')['transaction_qty'].transform('sum')
        
        return df
    
    @staticmethod
    def create_store_features(df: pd.DataFrame) -> pd.DataFrame:
        """Create store-related features.
        
        Args:
            df (pd.DataFrame): Input dataframe
            
        Returns:
            pd.DataFrame: DataFrame with additional store features
        """
        df = df.copy()
        
        # Store performance metrics
        df['store_daily_sales'] = df.groupby(['store_id', 'transaction_date'])['total_amount'].transform('sum')
        df['store_daily_transactions'] = df.groupby(['store_id', 'transaction_date'])['transaction_id'].transform('count')
        
        # Store product mix
        df['store_product_mix'] = df.groupby(['store_id', 'product_category'])['transaction_qty'].transform('sum')
        
        return df
