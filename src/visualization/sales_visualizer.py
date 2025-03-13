import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class SalesVisualizer:
    def __init__(self, output_dir: str = 'reports/figures'):
        """Initialize visualizer with output directory.
        
        Args:
            output_dir (str): Directory to save figures
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        plt.style.use('default')
        sns.set_theme(style="whitegrid")
    
    def plot_daily_sales_trend(self, df: pd.DataFrame, save: bool = True):
        """Plot daily sales trend."""
        plt.figure(figsize=(15, 6))
        daily_sales = df.groupby(df['datetime'].dt.date)['total_amount'].sum().reset_index()
        plt.plot(daily_sales['datetime'], daily_sales['total_amount'])
        plt.title('Daily Sales Trend')
        plt.xlabel('Date')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        if save:
            plt.savefig(self.output_dir / 'daily_sales_trend.png', bbox_inches='tight')
        plt.close()
    
    def plot_hourly_sales_pattern(self, df: pd.DataFrame, save: bool = True):
        """Plot hourly sales pattern."""
        plt.figure(figsize=(12, 6))
        hourly_sales = df.groupby('hour')['total_amount'].mean().reset_index()
        plt.bar(hourly_sales['hour'], hourly_sales['total_amount'])
        plt.title('Average Hourly Sales Pattern')
        plt.xlabel('Hour of Day')
        plt.ylabel('Average Sales ($)')
        if save:
            plt.savefig(self.output_dir / 'hourly_sales_pattern.png', bbox_inches='tight')
        plt.close()
    
    def plot_product_category_sales(self, df: pd.DataFrame, save: bool = True):
        """Plot sales by product category."""
        plt.figure(figsize=(10, 6))
        category_sales = df.groupby('product_category')['total_amount'].sum()
        category_sales.plot(kind='bar')
        plt.title('Sales by Product Category')
        plt.xlabel('Category')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        if save:
            plt.savefig(self.output_dir / 'category_sales.png', bbox_inches='tight')
        plt.close()
    
    def plot_store_performance(self, df: pd.DataFrame, save: bool = True):
        """Plot store performance comparison."""
        plt.figure(figsize=(12, 6))
        store_sales = df.groupby('store_location')['total_amount'].sum()
        store_sales.plot(kind='bar')
        plt.title('Total Sales by Store Location')
        plt.xlabel('Store Location')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        if save:
            plt.savefig(self.output_dir / 'store_performance.png', bbox_inches='tight')
        plt.close()
    
    def plot_sales_heatmap(self, df: pd.DataFrame, save: bool = True):
        """Plot sales heatmap by hour and day of week."""
        plt.figure(figsize=(12, 8))
        pivot_table = pd.pivot_table(
            df,
            values='total_amount',
            index='day_of_week',
            columns='hour',
            aggfunc='mean'
        )
        sns.heatmap(pivot_table, cmap='YlOrRd', annot=True, fmt='.0f')
        plt.title('Sales Heatmap: Hour vs Day of Week')
        if save:
            plt.savefig(self.output_dir / 'sales_heatmap.png', bbox_inches='tight')
        plt.close()
