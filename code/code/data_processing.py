import pandas as pd

class EVDataProcessor:
    def __init__(self, raw_path: str = 'Electric_Vehicle_Population_Data.csv'):
        self.raw_path = raw_path
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """Load raw data from CSV"""
        self.df = pd.read_csv(self.raw_path)
        return self.df

    def _parse_geopoint(self, point_str: str) -> tuple:
        """Helper to parse POINT strings into (lat, lon)"""
        try:
            if pd.notna(point_str) and 'POINT' in point_str:
                coords = point_str.split('(')[1].split(')')[0].split()
                return float(coords[1]), float(coords[0])  # Lat, Lon
            return (None, None)
        except (IndexError, ValueError):
            return (None, None)

    def transform_data(self) -> pd.DataFrame:
        """Clean and transform dataset"""
        # Parse geographic data
        self.df[['Latitude', 'Longitude']] = self.df['Vehicle Location'].apply(
            lambda x: pd.Series(self._parse_geopoint(x))
        
        # Convert numeric columns
        self.df['Model Year'] = pd.to_numeric(self.df['Model Year'], errors='coerce')
        self.df['Electric Range'] = pd.to_numeric(self.df['Electric Range'], errors='coerce')
        
        # Clean text columns
        self.df['Make'] = self.df['Make'].str.strip().str.upper()
        self.df['Model'] = self.df['Model'].str.strip().str.title()
        
        # Drop unnecessary columns
        self.df = self.df.drop(columns=['VIN (1-10)', 'DOL Vehicle ID', 'Vehicle Location'], errors='ignore')
        
        return self.df

    def save_processed_data(self, output_path: str = 'cache/processed_ev_data.parquet'):
        """Save processed data to Parquet format"""
        self.df.to_parquet(output_path)
        print(f"Saved processed data to {output_path}")

if __name__ == "__main__":
    # Run full processing pipeline
    processor = EVDataProcessor()
    processor.load_data()
    processor.transform_data()
    processor.save_processed_data()