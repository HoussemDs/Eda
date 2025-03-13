import pandas as pd
from datetime import datetime

class DataPreprocessor:
    @staticmethod
    def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess the coffee shop sales data.
        
        Args:
            df (pd.DataFrame): Raw data frame
            
        Returns:
            pd.DataFrame: Preprocessed data frame
        """
        df = df.copy()
        
        # Convert transaction_time to proper time format if it's not already
        if isinstance(df['transaction_time'].iloc[0], str):
            df['transaction_time'] = pd.to_datetime(df['transaction_time']).dt.time
        
        # Combine date and time into datetime
        df['datetime'] = pd.to_datetime(
            df['transaction_date'].astype(str) + ' ' + 
            df['transaction_time'].astype(str)
        )
        
        # Calculate total amount per transaction
        df['total_amount'] = df['transaction_qty'] * df['unit_price']
        
        # Extract time-based features
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.day_name()
        df['month'] = df['datetime'].dt.month_name()
        
        # Create time periods
        df['time_period'] = pd.cut(df['hour'],
                                 bins=[0, 11, 14, 17, 24],
                                 labels=['Morning', 'Lunch', 'Afternoon', 'Evening'])
        
        return df
        
    @staticmethod
    def check_data_quality(df: pd.DataFrame) -> dict:
        """Check data quality and return summary statistics.
        
        Args:
            df (pd.DataFrame): Input data frame
            
        Returns:
            dict: Data quality metrics
        """
        quality_metrics = {
            'total_rows': len(df),
            'missing_values': df.isnull().sum().to_dict(),
            'duplicates': df.duplicated().sum(),
            'unique_stores': df['store_id'].nunique(),
            'unique_products': df['product_id'].nunique(),
            'date_range': {
                'start': df['datetime'].min(),
                'end': df['datetime'].max()
            }
        }
        
        return quality_metrics
