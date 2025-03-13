import pandas as pd
from pathlib import Path

class DataLoader:
    def __init__(self, data_path: str):
        """Initialize DataLoader with path to data file.
        
        Args:
            data_path (str): Path to the Excel file
        """
        self.data_path = Path(data_path)
        
    def load_data(self) -> pd.DataFrame:
        """Load the coffee shop sales data from Excel file.
        
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            df = pd.read_excel(self.data_path)
            print(f"Successfully loaded {len(df)} records from {self.data_path}")
            return df
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise
