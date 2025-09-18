import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional

class CALFundExtractor:
    def __init__(self):
        self.base_url = "https://cal.lk/wp-admin/admin-ajax.php"
        self.target_fund_name = "Capital Alliance Quantitative Equity Fund"
        
    def generate_date_range(self) -> List[str]:
        """Generate list of dates for 1st and 15th of each month from June 2024 to September 2025"""
        dates = []
        start_date = datetime(2024, 6, 1)
        end_date = datetime(2025, 9, 1)
        
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
        """Collect price data for all dates in the range"""
        dates = self.generate_date_range()
        price_data = {}
        
        print(f"Fetching data for {len(dates)} dates...")
        
        for i, date in enumerate(dates, 1):
            print(f"Processing date {i}/{len(dates)}: {date}")
            
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
        plt.title(f'{self.target_fund_name}\nPrice Trend (OLD_PRICE) - 1st & 15th of Each Month', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price (LKR)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Format x-axis dates
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the graph
        plt.savefig('cal_fund_price_trend.png', dpi=300, bbox_inches='tight')
        print("Graph saved as 'cal_fund_price_trend.png'")
        
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
        
        csv_filename = 'cal_fund_data.csv'
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to '{csv_filename}'")

def main():
    """Main function to run the fund data extraction and visualization"""
    extractor = CALFundExtractor()
    
    print("CAL Fund Data Extractor")
    print("=" * 50)
    print(f"Target Fund: {extractor.target_fund_name}")
    print("Date Range: June 2024 - September 2025 (1st & 15th of each month)")
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
