import pandas as pd
import os
import requests
from pathlib import Path
import hashlib

class EVDataProcessor:
    def __init__(self, 
                 url: str = 'https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD',
                 raw_cache_path: str = 'cache/raw_ev_data.csv',
                 processed_cache_path: str = 'cache/processed_ev_data.parquet'):
        # Initialize the data processor with configuration
        # url: Source URL for EV data
        # raw_cache_path: Storage path for raw data
        # processed_cache_path: Storage path for processed data
        self.url = url
        self.raw_cache_path = raw_cache_path
        self.processed_cache_path = processed_cache_path
        self.df = None  # Will hold our DataFrame
        self._ensure_cache_dir()  # Create cache directories

    def _ensure_cache_dir(self):
        # Create cache directories if they don't exist
        # exist_ok=True prevents errors if directories exist
        os.makedirs(os.path.dirname(self.raw_cache_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.processed_cache_path), exist_ok=True)

    def _download_data(self) -> str:
        # Download raw data from the configured URL
        # Returns: Path to downloaded file
        # Raises: requests.exceptions.RequestException if download fails
        print(f"Downloading fresh data from {self.url}")
        response = requests.get(self.url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        # Write content to cache location
        with open(self.raw_cache_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Saved raw data to {self.raw_cache_path}")
        return self.raw_cache_path

    def _get_data_hash(self) -> str:
        # Calculate MD5 hash of raw data file
        # Returns: Hex digest of file hash, or empty string if no file
        if not os.path.exists(self.raw_cache_path):
            return ""
            
        # Calculate hash to detect file changes
        with open(self.raw_cache_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def load_data(self, force_download: bool = False) -> pd.DataFrame:
        # Load data from cache or download if needed
        # force_download: If True, always download fresh data
        # Returns: Loaded pandas DataFrame
        
        # Always download if forced or no cache exists
        if force_download or not os.path.exists(self.raw_cache_path):
            self._download_data()
        else:
            # Verify if remote data changed by comparing sizes
            try:
                response = requests.head(self.url)  # HEAD is faster than GET
                remote_size = int(response.headers.get('Content-Length', 0))
                local_size = os.path.getsize(self.raw_cache_path)
                
                if remote_size != local_size:
                    print("Data source changed - downloading fresh copy")
                    self._download_data()
            except Exception as e:
                print(f"Couldn't verify remote data: {e}. Using cached version.")

        # Load from cache (either existing or new)
        self.df = pd.read_csv(self.raw_cache_path)
        print(f"Loaded {len(self.df)} records from {self.raw_cache_path}")
        return self.df

    def _parse_geopoint(self, point_str: str) -> tuple:
        # Parse POINT string into (latitude, longitude)
        # point_str: String in format "POINT (lon lat)"
        # Returns: Tuple of (lat, lon) or (None, None) if fails
        try:
            if pd.notna(point_str) and 'POINT' in point_str:
                # Extract from string like "POINT (-122.123 47.456)"
                coords = point_str.split('(')[1].split(')')[0].split()
                # GeoJSON uses (lon, lat) but we return (lat, lon)
                return float(coords[1]), float(coords[0])  
            return (None, None)
        except (IndexError, ValueError) as e:
            print(f"Failed to parse geolocation: {e}")
            return (None, None)

    def transform_data(self) -> pd.DataFrame:
        # Clean and transform raw data into analysis-ready format
        # Processing steps:
        # 1. Parse geographic coordinates
        # 2. Convert numeric columns
        # 3. Clean text fields
        # 4. Remove unnecessary columns
        # Returns: Transformed DataFrame
        
        if self.df is None:
            self.load_data()
            
        # 1. Parse geographic data
        self.df[['Latitude', 'Longitude']] = self.df['Vehicle Location'].apply(
            lambda x: pd.Series(self._parse_geopoint(x))
        )

        # 2. Convert numeric columns with error handling
        self.df['Model Year'] = pd.to_numeric(self.df['Model Year'], errors='coerce')
        self.df['Electric Range'] = pd.to_numeric(self.df['Electric Range'], errors='coerce')
        
        # 3. Standardize text formatting
        self.df['Make'] = self.df['Make'].str.strip().str.upper()  # "tesla" -> "TESLA"
        self.df['Model'] = self.df['Model'].str.strip().str.title()  # "model s" -> "Model S"
        
        # 4. Remove unused columns
        self.df = self.df.drop(
            columns=['VIN (1-10)', 'DOL Vehicle ID', 'Vehicle Location'], 
            errors='ignore'  # Skip if columns don't exist
        )
        
        print("Data transformation complete")
        return self.df

    def save_processed_data(self, output_path: str = None) -> str:
        # Save processed data to Parquet format
        # output_path: Optional custom path to save data
        # Returns: Path to saved file
        
        if self.df is None:
            self.transform_data()
            
        # Use provided path or default to configured path
        save_path = output_path if output_path else self.processed_cache_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self.df.to_parquet(save_path)
        print(f"Saved {len(self.df)} records to {save_path}")
        return save_path

    def get_processed_data(self, force_refresh: bool = False) -> pd.DataFrame:
        # Get processed data using cache if available
        # force_refresh: If True, reprocess data even if cached exists
        # Returns: Processed DataFrame ready for analysis
        
        # Try loading cached data unless forced to refresh
        if not force_refresh and os.path.exists(self.processed_cache_path):
            try:
                cached_data = pd.read_parquet(self.processed_cache_path)
                print(f"Loaded cached data ({len(cached_data)} records)")
                return cached_data
            except Exception as e:
                print(f"Error loading cache: {e}. Reprocessing...")
                
        # Full processing pipeline if cache unavailable/invalid
        self.load_data()
        self.transform_data()
        self.save_processed_data()  # Saves to default location
        return self.df


if __name__ == "__main__":
    # Example usage when run directly
    print("Running EV data processing pipeline...")
    
    # Initialize with default settings
    processor = EVDataProcessor()
    
    # Get processed data (uses cache if available)
    df = processor.get_processed_data()