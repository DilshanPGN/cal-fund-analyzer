#!/usr/bin/env python3
"""
CAL Fund PNG Updater

A standalone script to generate PNG visualizations from existing CSV files.
This script can be used to:
1. Generate PNG files for all existing CSV files
2. Update PNG files for specific CSV files
3. Monitor CSV files and automatically update PNGs when they change

Usage:
    python png_updater.py                    # Update all CSV files
    python png_updater.py --file filename.csv  # Update specific file
    python png_updater.py --monitor          # Monitor for changes
    python png_updater.py --help             # Show help
"""

import os
import sys
import argparse
import time
import glob
from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Optional
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CALFundPNGUpdater:
    """Standalone PNG updater for CAL Fund CSV files"""
    
    def __init__(self):
        self.csv_pattern = "cal_fund_data_*.csv"
        self.png_pattern = "cal_fund_price_trend_*.png"
        
    def get_fund_name_from_filename(self, csv_filename: str) -> str:
        """Extract fund name from CSV filename"""
        # Remove path and extension
        filename = os.path.basename(csv_filename)
        if filename.startswith("cal_fund_data_"):
            fund_name = filename[14:-4]  # Remove "cal_fund_data_" and ".csv"
            # Convert underscores back to spaces and slashes
            fund_name = fund_name.replace("_", " ").replace("  ", "/")
            return fund_name
        return "Unknown Fund"
    
    def generate_png_from_csv(self, csv_filename: str) -> bool:
        """Generate PNG visualization from CSV file"""
        if not os.path.exists(csv_filename):
            print(f"❌ CSV file not found: {csv_filename}")
            return False
        
        try:
            # Read CSV data
            df = pd.read_csv(csv_filename)
            if 'Date' not in df.columns or 'OLD_PRICE' not in df.columns:
                print(f"❌ Invalid CSV format in {csv_filename}")
                return False
            
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
            
            if len(df) == 0:
                print(f"❌ No data to visualize in {csv_filename}")
                return False
            
            # Get fund name
            fund_name = self.get_fund_name_from_filename(csv_filename)
            
            # Create the plot
            plt.figure(figsize=(12, 8))
            plt.plot(df['Date'], df['OLD_PRICE'], marker='o', linewidth=2, markersize=4, alpha=0.7, color='#1f77b4')
            
            # Set up the plot
            plt.title(f'{fund_name}\nPrice Trend Analysis', fontsize=14, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Price (LKR)', fontsize=12)
            plt.grid(True, alpha=0.3)
            
            # Format x-axis dates
            plt.xticks(rotation=45)
            
            # Generate PNG filename
            png_filename = csv_filename.replace('.csv', '.png').replace('cal_fund_data_', 'cal_fund_price_trend_')
            
            # Save as high-resolution PNG
            plt.tight_layout()
            plt.savefig(png_filename, dpi=300, bbox_inches='tight')
            plt.close()  # Close the figure to free memory
            
            print(f"✅ PNG visualization saved to '{png_filename}'")
            return True
            
        except Exception as e:
            print(f"❌ Error generating PNG from {csv_filename}: {e}")
            plt.close()  # Ensure figure is closed even on error
            return False
    
    def find_csv_files(self) -> List[str]:
        """Find all CAL fund CSV files in current directory"""
        csv_files = glob.glob(self.csv_pattern)
        return sorted(csv_files)
    
    def find_png_files(self) -> List[str]:
        """Find all CAL fund PNG files in current directory"""
        png_files = glob.glob(self.png_pattern)
        return sorted(png_files)
    
    def update_all_csv_files(self) -> Dict[str, bool]:
        """Update PNG files for all CSV files"""
        csv_files = self.find_csv_files()
        
        if not csv_files:
            print("❌ No CAL fund CSV files found in current directory")
            print(f"   Looking for files matching pattern: {self.csv_pattern}")
            return {}
        
        print(f"🔄 Found {len(csv_files)} CSV files to process:")
        for csv_file in csv_files:
            fund_name = self.get_fund_name_from_filename(csv_file)
            print(f"   📊 {fund_name}")
        
        print("\n" + "="*60)
        
        results = {}
        successful = 0
        failed = 0
        
        for i, csv_file in enumerate(csv_files, 1):
            fund_name = self.get_fund_name_from_filename(csv_file)
            print(f"\n[{i}/{len(csv_files)}] Processing: {fund_name}")
            print(f"   📁 CSV: {csv_file}")
            
            success = self.generate_png_from_csv(csv_file)
            results[csv_file] = success
            
            if success:
                successful += 1
            else:
                failed += 1
        
        print("\n" + "="*60)
        print(f"📊 Summary:")
        print(f"   ✅ Successful: {successful}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📁 Total processed: {len(csv_files)}")
        
        return results
    
    def update_specific_file(self, csv_filename: str) -> bool:
        """Update PNG file for a specific CSV file"""
        if not csv_filename.endswith('.csv'):
            csv_filename += '.csv'
        
        fund_name = self.get_fund_name_from_filename(csv_filename)
        print(f"🔄 Processing: {fund_name}")
        print(f"   📁 CSV: {csv_filename}")
        
        return self.generate_png_from_csv(csv_filename)
    
    def get_file_status(self) -> Dict[str, Dict[str, str]]:
        """Get status of CSV and PNG files"""
        csv_files = self.find_csv_files()
        png_files = self.find_png_files()
        
        status = {}
        
        for csv_file in csv_files:
            fund_name = self.get_fund_name_from_filename(csv_file)
            png_file = csv_file.replace('.csv', '.png').replace('cal_fund_data_', 'cal_fund_price_trend_')
            
            csv_mtime = datetime.fromtimestamp(os.path.getmtime(csv_file))
            
            if os.path.exists(png_file):
                png_mtime = datetime.fromtimestamp(os.path.getmtime(png_file))
                if csv_mtime > png_mtime:
                    status[csv_file] = {
                        'fund_name': fund_name,
                        'status': 'needs_update',
                        'csv_modified': csv_mtime.strftime('%Y-%m-%d %H:%M:%S'),
                        'png_modified': png_mtime.strftime('%Y-%m-%d %H:%M:%S')
                    }
                else:
                    status[csv_file] = {
                        'fund_name': fund_name,
                        'status': 'up_to_date',
                        'csv_modified': csv_mtime.strftime('%Y-%m-%d %H:%M:%S'),
                        'png_modified': png_mtime.strftime('%Y-%m-%d %H:%M:%S')
                    }
            else:
                status[csv_file] = {
                    'fund_name': fund_name,
                    'status': 'missing_png',
                    'csv_modified': csv_mtime.strftime('%Y-%m-%d %H:%M:%S'),
                    'png_modified': 'N/A'
                }
        
        return status
    
    def show_status(self):
        """Show status of all CSV and PNG files"""
        status = self.get_file_status()
        
        if not status:
            print("❌ No CAL fund CSV files found in current directory")
            return
        
        print("📊 CAL Fund File Status:")
        print("="*80)
        
        needs_update = []
        up_to_date = []
        missing_png = []
        
        for csv_file, info in status.items():
            if info['status'] == 'needs_update':
                needs_update.append((csv_file, info))
            elif info['status'] == 'up_to_date':
                up_to_date.append((csv_file, info))
            else:
                missing_png.append((csv_file, info))
        
        if needs_update:
            print(f"\n🔄 Files needing PNG update ({len(needs_update)}):")
            for csv_file, info in needs_update:
                print(f"   📊 {info['fund_name']}")
                print(f"      📁 CSV: {csv_file}")
                print(f"      📅 CSV modified: {info['csv_modified']}")
                print(f"      📅 PNG modified: {info['png_modified']}")
                print()
        
        if missing_png:
            print(f"\n❌ Files missing PNG ({len(missing_png)}):")
            for csv_file, info in missing_png:
                print(f"   📊 {info['fund_name']}")
                print(f"      📁 CSV: {csv_file}")
                print(f"      📅 CSV modified: {info['csv_modified']}")
                print()
        
        if up_to_date:
            print(f"\n✅ Files up to date ({len(up_to_date)}):")
            for csv_file, info in up_to_date:
                print(f"   📊 {info['fund_name']}")
                print(f"      📁 CSV: {csv_file}")
                print(f"      📅 Last modified: {info['csv_modified']}")
                print()


class CSVFileHandler(FileSystemEventHandler):
    """File system event handler for CSV file monitoring"""
    
    def __init__(self, updater: CALFundPNGUpdater):
        self.updater = updater
        self.last_modified = {}
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Only process CSV files
        if not file_path.endswith('.csv') or not os.path.basename(file_path).startswith('cal_fund_data_'):
            return
        
        # Avoid duplicate events (file systems can fire multiple events)
        current_time = time.time()
        if file_path in self.last_modified:
            if current_time - self.last_modified[file_path] < 2:  # 2 second debounce
                return
        
        self.last_modified[file_path] = current_time
        
        print(f"\n🔄 Detected change in: {os.path.basename(file_path)}")
        fund_name = self.updater.get_fund_name_from_filename(file_path)
        print(f"   📊 Fund: {fund_name}")
        
        # Generate PNG
        success = self.updater.generate_png_from_csv(file_path)
        if success:
            print(f"   ✅ PNG updated successfully")
        else:
            print(f"   ❌ PNG update failed")


def monitor_csv_files(updater: CALFundPNGUpdater):
    """Monitor CSV files for changes and auto-update PNGs"""
    print("🔍 Starting CSV file monitoring...")
    print("   📁 Monitoring current directory for CAL fund CSV files")
    print("   🖼️ PNG files will be automatically updated when CSV files change")
    print("   ⏹️ Press Ctrl+C to stop monitoring")
    print("="*60)
    
    event_handler = CSVFileHandler(updater)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️ Stopping file monitoring...")
        observer.stop()
    
    observer.join()
    print("✅ File monitoring stopped")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="CAL Fund PNG Updater - Generate PNG visualizations from CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python png_updater.py                    # Update all CSV files
  python png_updater.py --file fund.csv  # Update specific file
  python png_updater.py --monitor        # Monitor for changes
  python png_updater.py --status         # Show file status
  python png_updater.py --help           # Show this help
        """
    )
    
    parser.add_argument('--file', '-f', 
                       help='Update PNG for specific CSV file')
    parser.add_argument('--monitor', '-m', action='store_true',
                       help='Monitor CSV files and auto-update PNGs')
    parser.add_argument('--status', '-s', action='store_true',
                       help='Show status of CSV and PNG files')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Update PNG files for all CSV files')
    
    args = parser.parse_args()
    
    updater = CALFundPNGUpdater()
    
    print("CAL Fund PNG Updater")
    print("="*50)
    
    if args.status:
        updater.show_status()
    elif args.monitor:
        # Check if watchdog is available
        try:
            import watchdog
            monitor_csv_files(updater)
        except ImportError:
            print("❌ Error: 'watchdog' package is required for file monitoring")
            print("   Install it with: pip install watchdog")
            sys.exit(1)
    elif args.file:
        success = updater.update_specific_file(args.file)
        sys.exit(0 if success else 1)
    elif args.all or len(sys.argv) == 1:
        # Default behavior: update all files
        results = updater.update_all_csv_files()
        if not results:
            sys.exit(1)
        
        # Check if any failed
        failed_count = sum(1 for success in results.values() if not success)
        sys.exit(0 if failed_count == 0 else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
