import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

def analyze_sales(excel_file: str):
    """Analyze coffee shop sales data and generate insights."""
    print("Starting Coffee Shop Sales Analysis...")
    
    # 1. Load and prepare data
    print("\n1. Loading data...")
    df = pd.read_excel(excel_file)
    print(f"Loaded {len(df)} records")
    
    # 2. Process datetime
    print("\n2. Processing datetime...")
    df['datetime'] = pd.to_datetime(
        df['transaction_date'].astype(str) + ' ' + 
        df['transaction_time'].astype(str)
    )
    
    # 3. Create basic features
    print("\n3. Creating features...")
    df['total_amount'] = df['transaction_qty'] * df['unit_price']
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['month'] = df['datetime'].dt.month_name()
    
    # 4. Basic sales analysis
    print("\n4. Analyzing sales...")
    total_sales = df['total_amount'].sum()
    avg_daily_sales = df.groupby(df['datetime'].dt.date)['total_amount'].sum().mean()
    peak_hour = df.groupby('hour')['total_amount'].sum().idxmax()
    best_category = df.groupby('product_category')['total_amount'].sum().idxmax()
    best_store = df.groupby('store_location')['total_amount'].sum().idxmax()
    
    print(f"\nKey Metrics:")
    print(f"- Total Sales: ${total_sales:,.2f}")
    print(f"- Average Daily Sales: ${avg_daily_sales:,.2f}")
    print(f"- Peak Sales Hour: {peak_hour}:00")
    print(f"- Best Performing Category: {best_category}")
    print(f"- Best Performing Store: {best_store}")
    
    # 5. Create visualizations
    print("\n5. Generating visualizations...")
    reports_dir = Path('reports/figures')
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # 5.1 Daily Sales Trend
    plt.figure(figsize=(15, 6))
    daily_sales = df.groupby(df['datetime'].dt.date)['total_amount'].sum()
    daily_sales.plot(kind='line')
    plt.title('Daily Sales Trend')
    plt.xlabel('Date')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(reports_dir / 'daily_sales_trend.png')
    plt.close()
    
    # 5.2 Product Category Sales
    plt.figure(figsize=(10, 6))
    category_sales = df.groupby('product_category')['total_amount'].sum()
    category_sales.plot(kind='bar')
    plt.title('Sales by Product Category')
    plt.xlabel('Category')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(reports_dir / 'category_sales.png')
    plt.close()
    
    # 5.3 Store Performance
    plt.figure(figsize=(12, 6))
    store_sales = df.groupby('store_location')['total_amount'].sum()
    store_sales.plot(kind='bar')
    plt.title('Sales by Store Location')
    plt.xlabel('Store')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(reports_dir / 'store_sales.png')
    plt.close()
    
    # 5.4 Hourly Pattern
    plt.figure(figsize=(12, 6))
    hourly_sales = df.groupby('hour')['total_amount'].mean()
    hourly_sales.plot(kind='bar')
    plt.title('Average Sales by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Sales ($)')
    plt.tight_layout()
    plt.savefig(reports_dir / 'hourly_pattern.png')
    plt.close()
    
    print("\nAnalysis complete! Check the 'reports/figures' directory for visualizations.")

if __name__ == "__main__":
    analyze_sales('Coffee Shop Sales.xlsx')
