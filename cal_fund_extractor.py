import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import os
from typing import List, Dict, Optional

class CALFundExtractor:
    def __init__(self, fund_name: str = None, start_date: str = None, end_date: str = None):
        self.base_url = "https://cal.lk/wp-admin/admin-ajax.php"
        self.target_fund_name = fund_name or "Capital Alliance Quantitative Equity Fund"
        self.start_date = start_date or "2024-06-01"
        self.end_date = end_date or "2025-09-01"
        self.csv_filename = f'cal_fund_data_{self.target_fund_name.replace(" ", "_").replace("/", "_")}.csv'
        
    def generate_date_range(self) -> List[str]:
        """Generate list of dates for 1st and 15th of each month within the specified date range"""
        dates = []
        try:
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date, "%Y-%m-%d")
        except ValueError as e:
            print(f"Invalid date format. Please use YYYY-MM-DD format. Error: {e}")
            return []
        
        current_date = start_date
        while current_date <= end_date:
            # Add 1st of the month
            dates.append(current_date.strftime("%Y-%m-%d"))
            
            # Add 15th of the month (if it exists and is within range)
            fifteenth = current_date.replace(day=15)
            if fifteenth <= end_date:
                dates.append(fifteenth.strftime("%Y-%m-%d"))
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        return dates
    
    def discover_available_funds(self, sample_date: str = "2024-06-01") -> List[str]:
        """Discover all available funds from the API"""
        print(f"Discovering available funds using sample date: {sample_date}")
        
        fund_data = self.fetch_fund_data(sample_date)
        if not fund_data or 'UTMS_FUND' not in fund_data:
            print("Failed to fetch fund data for discovery")
            return []
        
        available_funds = []
        for fund in fund_data['UTMS_FUND']:
            fund_name = fund.get('FUND_NAME')
            if fund_name:
                available_funds.append(fund_name)
        
        print(f"Found {len(available_funds)} available funds")
        return available_funds
    
    def load_existing_data(self) -> Dict[str, float]:
        """Load existing data from CSV file if it exists"""
        if not os.path.exists(self.csv_filename):
            print(f"No existing data file found: {self.csv_filename}")
            return {}
        
        try:
            df = pd.read_csv(self.csv_filename)
            if 'Date' in df.columns and 'OLD_PRICE' in df.columns:
                # Convert to dictionary with date as key and price as value
                existing_data = dict(zip(df['Date'].astype(str), df['OLD_PRICE']))
                print(f"Loaded {len(existing_data)} existing data points from {self.csv_filename}")
                return existing_data
            else:
                print(f"Invalid CSV format in {self.csv_filename}")
                return {}
        except Exception as e:
            print(f"Error loading existing data from {self.csv_filename}: {e}")
            return {}
    
    def fetch_fund_data(self, date: str) -> Optional[Dict]:
        """Fetch fund data for a specific date"""
        params = {
            'action': 'getUTFundRates',
            'valuedate': date
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for date {date}: {e}")
            return None
    
    def extract_target_fund_price(self, fund_data: Dict, date: str) -> Optional[float]:
        """Extract OLD_PRICE for the target fund from fund data"""
        if not fund_data or 'UTMS_FUND' not in fund_data:
            return None
        
        for fund in fund_data['UTMS_FUND']:
            if fund.get('FUND_NAME') == self.target_fund_name:
                try:
                    return float(fund.get('OLD_PRICE', 0))
                except (ValueError, TypeError):
                    print(f"Invalid price data for {self.target_fund_name} on {date}")
                    return None
        
        print(f"Fund '{self.target_fund_name}' not found for date {date}")
        return None
    
    def collect_price_data(self) -> Dict[str, float]:
        """Collect price data for all dates in the range, using cached data when available"""
        # Load existing data first
        price_data = self.load_existing_data()
        
        dates = self.generate_date_range()
        missing_dates = [date for date in dates if date not in price_data]
        
        if missing_dates:
            print(f"Found {len(price_data)} existing data points")
            print(f"Fetching data for {len(missing_dates)} missing dates...")
            
            for i, date in enumerate(missing_dates, 1):
                print(f"Processing missing date {i}/{len(missing_dates)}: {date}")
                
                fund_data = self.fetch_fund_data(date)
                if fund_data:
                    price = self.extract_target_fund_price(fund_data, date)
                    if price is not None:
                        price_data[date] = price
                        print(f"  ✓ Price: {price}")
                    else:
                        print(f"  ✗ No price data found")
                else:
                    print(f"  ✗ Failed to fetch data")
                
                # Add small delay to be respectful to the API
                time.sleep(0.5)
        else:
            print(f"All {len(dates)} dates already have data - no API calls needed!")
        
        return price_data
    
    def create_graph(self, price_data: Dict[str, float]):
        """Create a graph showing date vs OLD_PRICE"""
        if not price_data:
            print("No data available to create graph")
            return
        
        # Convert to DataFrame for easier handling
        df = pd.DataFrame(list(price_data.items()), columns=['Date', 'Price'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        # Create the plot
        plt.figure(figsize=(15, 8))
        plt.plot(df['Date'], df['Price'], marker='o', linewidth=2, markersize=6)
        plt.title(f'{self.target_fund_name}\nPrice Trend (OLD_PRICE) - {self.start_date} to {self.end_date}', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price (LKR)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Format x-axis dates
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the graph
        graph_filename = f'cal_fund_price_trend_{self.target_fund_name.replace(" ", "_").replace("/", "_")}.png'
        plt.savefig(graph_filename, dpi=300, bbox_inches='tight')
        print(f"Graph saved as '{graph_filename}'")
        
        # Show the graph
        plt.show()
        
        # Print summary statistics
        print(f"\nSummary Statistics:")
        print(f"Total data points: {len(df)}")
        print(f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
        print(f"Price range: {df['Price'].min():.4f} to {df['Price'].max():.4f}")
        print(f"Average price: {df['Price'].mean():.4f}")
    
    def save_data_to_csv(self, price_data: Dict[str, float]):
        """Save the collected data to CSV file"""
        if not price_data:
            print("No data to save")
            return
        
        df = pd.DataFrame(list(price_data.items()), columns=['Date', 'OLD_PRICE'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        df.to_csv(self.csv_filename, index=False)
        print(f"Data saved to '{self.csv_filename}'")

def get_user_fund_selection(available_funds: List[str]) -> str:
    """Get fund selection from user"""
    print("\nAvailable Funds:")
    print("-" * 50)
    for i, fund in enumerate(available_funds, 1):
        print(f"{i:2d}. {fund}")
    
    while True:
        try:
            choice = input(f"\nSelect a fund (1-{len(available_funds)}) or press Enter for default: ").strip()
            if not choice:
                return "Capital Alliance Quantitative Equity Fund"
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_funds):
                return available_funds[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(available_funds)}")
        except ValueError:
            print("Please enter a valid number")

def get_user_date_input(prompt: str, default: str) -> str:
    """Get date input from user with validation"""
    while True:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        if not user_input:
            return default
        
        try:
            # Validate date format
            datetime.strptime(user_input, "%Y-%m-%d")
            return user_input
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format (e.g., 2024-06-01)")

def main():
    """Main function to run the fund data extraction and visualization"""
    print("CAL Fund Data Extractor")
    print("=" * 50)
    
    # Create a temporary extractor to discover available funds
    temp_extractor = CALFundExtractor()
    available_funds = temp_extractor.discover_available_funds()
    
    if not available_funds:
        print("Failed to discover available funds. Using default fund.")
        selected_fund = "Capital Alliance Quantitative Equity Fund"
    else:
        selected_fund = get_user_fund_selection(available_funds)
    
    # Get date range from user
    start_date = get_user_date_input("Enter start date (YYYY-MM-DD)", "2024-06-01")
    end_date = get_user_date_input("Enter end date (YYYY-MM-DD)", "2025-09-01")
    
    # Create the main extractor with user selections
    extractor = CALFundExtractor(selected_fund, start_date, end_date)
    
    print("\n" + "=" * 50)
    print(f"Target Fund: {extractor.target_fund_name}")
    print(f"Date Range: {extractor.start_date} - {extractor.end_date} (1st & 15th of each month)")
    print(f"Data will be saved to: {extractor.csv_filename}")
    print("=" * 50)
    
    # Collect price data
    price_data = extractor.collect_price_data()
    
    if price_data:
        print(f"\nSuccessfully collected {len(price_data)} data points")
        
        # Save data to CSV
        extractor.save_data_to_csv(price_data)
        
        # Create and display graph
        extractor.create_graph(price_data)
        
        # Display raw data
        print(f"\nRaw Data:")
        print("-" * 30)
        for date, price in sorted(price_data.items()):
            print(f"{date}: {price:.4f}")
    else:
        print("No data was collected. Please check the API endpoint and try again.")

if __name__ == "__main__":
    main()
