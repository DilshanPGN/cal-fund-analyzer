import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import time
import os
import sys
from typing import List, Dict, Optional
import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, scrolledtext

class CALFundExtractor:
    def __init__(self, fund_name: str = None, start_date: str = None, end_date: str = None, api_delay: float = None):
        self.base_url = "https://cal.lk/wp-admin/admin-ajax.php"
        self.target_fund_name = fund_name or "Capital Alliance Quantitative Equity Fund"
        
        # Set default dates: start from 2013-01-01, end at current date - 1
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.start_date = start_date or "2013-01-01"
        self.end_date = end_date or yesterday
        
        # Set default API delay: 0.5 seconds
        self.api_delay = api_delay or 0.5
        
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
    
    def discover_available_funds(self, sample_date: str = None) -> List[str]:
        """Discover all available funds from the API"""
        # Use current date - 10 if no sample date provided
        if sample_date is None:
            sample_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        
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
    
    def get_fund_earliest_date(self, fund_name: str) -> str:
        """Get the earliest date available for a specific fund from its CSV file"""
        csv_filename = f'cal_fund_data_{fund_name.replace(" ", "_").replace("/", "_")}.csv'
        
        if not os.path.exists(csv_filename):
            print(f"No CSV file found for {fund_name}, using default start date")
            return "2013-01-01"
        
        try:
            df = pd.read_csv(csv_filename)
            if 'Date' in df.columns and len(df) > 0:
                df['Date'] = pd.to_datetime(df['Date'])
                earliest_date = df['Date'].min().strftime("%Y-%m-%d")
                print(f"Found earliest date for {fund_name}: {earliest_date}")
                return earliest_date
            else:
                print(f"Invalid CSV format for {fund_name}, using default start date")
                return "2013-01-01"
        except Exception as e:
            print(f"Error reading CSV for {fund_name}: {e}, using default start date")
            return "2013-01-01"
    
    def get_all_funds_earliest_dates(self) -> Dict[str, str]:
        """Get the earliest date for all available funds"""
        available_funds = self.discover_available_funds()
        earliest_dates = {}
        
        print(f"\nDetecting earliest dates for {len(available_funds)} funds:")
        print("-" * 50)
        
        for fund_name in available_funds:
            earliest_date = self.get_fund_earliest_date(fund_name)
            earliest_dates[fund_name] = earliest_date
        
        return earliest_dates
    
    def load_existing_data(self) -> Dict[str, float]:
        """Load existing data from CSV file if it exists, filtered by current date range"""
        if not os.path.exists(self.csv_filename):
            print(f"No existing data file found: {self.csv_filename}")
            return {}
        
        try:
            df = pd.read_csv(self.csv_filename)
            if 'Date' in df.columns and 'OLD_PRICE' in df.columns:
                # Convert dates to datetime for comparison
                df['Date'] = pd.to_datetime(df['Date'])
                
                # Filter data to only include dates within the current requested range
                start_date = pd.to_datetime(self.start_date)
                end_date = pd.to_datetime(self.end_date)
                
                # Filter the dataframe to only include dates within the current range
                filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
                
                # Convert to dictionary with date as key and price as value
                existing_data = dict(zip(filtered_df['Date'].dt.strftime('%Y-%m-%d'), filtered_df['OLD_PRICE']))
                
                total_points = len(df)
                filtered_points = len(existing_data)
                
                if total_points > filtered_points:
                    print(f"Loaded {filtered_points} existing data points from {self.csv_filename} (filtered from {total_points} total points)")
                else:
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
        existing_dates = [date for date in dates if date in price_data]
        
        # Show data coverage summary
        print(f"\nData Coverage Summary:")
        print(f"  Total dates in range: {len(dates)}")
        print(f"  Existing data points: {len(existing_dates)}")
        print(f"  Missing data points: {len(missing_dates)}")
        
        if existing_dates:
            print(f"  Existing data range: {min(existing_dates)} to {max(existing_dates)}")
            print(f"  ✓ Using cached data for {len(existing_dates)} dates")
        
        if missing_dates:
            print(f"  Missing data range: {min(missing_dates)} to {max(missing_dates)}")
            print(f"  🔄 Fetching from API for {len(missing_dates)} dates...")
            
            successful_fetches = 0
            skipped_dates = 0
            
            for i, date in enumerate(missing_dates, 1):
                print(f"  Processing missing date {i}/{len(missing_dates)}: {date}")
                
                fund_data = self.fetch_fund_data(date)
                if fund_data:
                    price = self.extract_target_fund_price(fund_data, date)
                    if price is not None and price > 0:  # Only store valid prices
                        price_data[date] = price
                        successful_fetches += 1
                        print(f"    ✓ Price: {price}")
                    else:
                        skipped_dates += 1
                        print(f"    ⚠ No valid price data - skipping date")
                else:
                    skipped_dates += 1
                    print(f"    ⚠ Failed to fetch data - skipping date")
                
                # Add configurable delay to be respectful to the API
                time.sleep(self.api_delay)
            
            print(f"\nFetch Summary:")
            print(f"  ✓ Successfully fetched: {successful_fetches} dates")
            print(f"  ⚠ Skipped (no data): {skipped_dates} dates")
        else:
            print(f"  ✅ All {len(dates)} dates already have data - no API calls needed!")
        
        print(f"\nFinal dataset: {len(price_data)} total data points")
        return price_data
    
    def create_graph(self, price_data: Dict[str, float]):
        """Create an interactive graph with manual UI"""
        if not price_data:
            print("No data available to create graph")
            return
        
        # Convert to DataFrame for easier handling
        df = pd.DataFrame(list(price_data.items()), columns=['Date', 'Price'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        # Create the manual UI
        self._create_manual_ui(df, price_data)
    
    def _create_manual_ui(self, df: pd.DataFrame, price_data: Dict[str, float]):
        """Create a manual tkinter UI with embedded matplotlib graph"""
        # Create main window
        self.root = tk.Tk()
        self.root.title(f"CAL Fund Analyzer - {self.target_fund_name}")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Store data for analysis
        self.df = df
        self.price_data = price_data
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel for controls
        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Create right panel for graph
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Add title
        title_label = ttk.Label(left_panel, text="Financial Context Analysis", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Add fund info
        fund_info = ttk.Label(left_panel, text=f"Fund: {self.target_fund_name}", 
                             font=('Arial', 10), wraplength=280)
        fund_info.pack(pady=(0, 10))
        
        # Add data summary
        summary_text = f"""Data Summary:
• Total Points: {len(df)}
• Date Range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}
• Price Range: {df['Price'].min():.4f} to {df['Price'].max():.4f}
• Average Price: {df['Price'].mean():.4f}"""
        
        summary_label = ttk.Label(left_panel, text=summary_text, 
                                  font=('Arial', 9), justify=tk.LEFT)
        summary_label.pack(pady=(0, 20))
        
        # Add analysis buttons
        self._create_analysis_buttons(left_panel)
        
        # Add date range controls
        self._create_date_controls(left_panel)
        
        # Add help section
        self._create_help_section(left_panel)
        
        # Create matplotlib graph
        self._create_matplotlib_graph(right_panel)
        
        # Start the UI
        self.root.mainloop()
    
    def _create_analysis_buttons(self, parent):
        """Create analysis buttons"""
        # Analysis buttons frame
        buttons_frame = ttk.LabelFrame(parent, text="Analysis Options", padding="10")
        buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Button styles
        button_style = {'width': 25}
        
        # Analyze Current View button
        self.analyze_current_btn = ttk.Button(buttons_frame, text="🔍 Analyze Current View", 
                                            command=self._analyze_current_view, **button_style)
        self.analyze_current_btn.pack(pady=2)
        
        # Crisis Period button
        self.crisis_btn = ttk.Button(buttons_frame, text="🚨 Crisis Period (2022)", 
                                   command=self._analyze_crisis_period, **button_style)
        self.crisis_btn.pack(pady=2)
        
        # Recovery Period button
        self.recovery_btn = ttk.Button(buttons_frame, text="📈 Recovery Period (2023)", 
                                     command=self._analyze_recovery_period, **button_style)
        self.recovery_btn.pack(pady=2)
        
        # Recent Performance button
        self.recent_btn = ttk.Button(buttons_frame, text="📊 Recent 6 Months", 
                                   command=self._analyze_recent_performance, **button_style)
        self.recent_btn.pack(pady=2)
        
        # Custom Range button
        self.custom_btn = ttk.Button(buttons_frame, text="📅 Custom Date Range", 
                                   command=self._analyze_custom_range, **button_style)
        self.custom_btn.pack(pady=2)
    
    def _create_date_controls(self, parent):
        """Create date range controls"""
        # Date controls frame
        date_frame = ttk.LabelFrame(parent, text="Date Range Controls", padding="10")
        date_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Start date
        ttk.Label(date_frame, text="Start Date:").pack(anchor=tk.W)
        self.start_date_var = tk.StringVar(value=self.df['Date'].min().strftime('%Y-%m-%d'))
        start_date_entry = ttk.Entry(date_frame, textvariable=self.start_date_var, width=15)
        start_date_entry.pack(pady=(0, 10))
        
        # End date
        ttk.Label(date_frame, text="End Date:").pack(anchor=tk.W)
        self.end_date_var = tk.StringVar(value=self.df['Date'].max().strftime('%Y-%m-%d'))
        end_date_entry = ttk.Entry(date_frame, textvariable=self.end_date_var, width=15)
        end_date_entry.pack(pady=(0, 10))
        
        # Update graph button
        update_btn = ttk.Button(date_frame, text="Update Graph", 
                               command=self._update_graph_range, width=20)
        update_btn.pack(pady=5)
    
    def _create_help_section(self, parent):
        """Create help section"""
        # Help frame
        help_frame = ttk.LabelFrame(parent, text="Help & Instructions", padding="10")
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = """Graph Controls:
• Mouse wheel: Zoom in/out
• Click & drag: Pan around
• Right-click: Reset view

Analysis Features:
• Click any analysis button to get financial context
• Use date controls to filter the graph
• All analysis results open in popup windows

Tips:
• Zoom into interesting periods first
• Use 'Analyze Current View' for zoomed areas
• Check crisis/recovery periods for context"""
        
        help_label = ttk.Label(help_frame, text=help_text, 
                              font=('Arial', 9), justify=tk.LEFT, wraplength=280)
        help_label.pack(fill=tk.BOTH, expand=True)
    
    def _create_matplotlib_graph(self, parent):
        """Create embedded matplotlib graph"""
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        
        # Plot the data
        self.line, = self.ax.plot(self.df['Date'], self.df['Price'], 
                                 marker='o', linewidth=2, markersize=4, alpha=0.7)
        
        # Set up the plot
        self.ax.set_title(f'{self.target_fund_name}\nPrice Trend Analysis', 
                         fontsize=14, fontweight='bold')
        self.ax.set_xlabel('Date', fontsize=12)
        self.ax.set_ylabel('Price (LKR)', fontsize=12)
        self.ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Create canvas and embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(self.canvas, parent)
        toolbar.update()
    
    def _update_graph_range(self):
        """Update graph with new date range"""
        try:
            start_date = pd.to_datetime(self.start_date_var.get())
            end_date = pd.to_datetime(self.end_date_var.get())
            
            # Filter data
            filtered_df = self.df[(self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)]
            
            if len(filtered_df) == 0:
                messagebox.showerror("Error", "No data found in the specified date range")
                return
            
            # Update the plot
            self.line.set_data(filtered_df['Date'], filtered_df['Price'])
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()
            
            messagebox.showinfo("Success", f"Graph updated with {len(filtered_df)} data points")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid date format: {e}")
    
    def _analyze_current_view(self):
        """Analyze the currently visible area of the graph"""
        try:
            # Get current x-axis limits
            xlim = self.ax.get_xlim()
            start_date = pd.to_datetime(xlim[0], unit='D').strftime('%Y-%m-%d')
            end_date = pd.to_datetime(xlim[1], unit='D').strftime('%Y-%m-%d')
            
            # Filter data for current view
            filtered_data = {date: price for date, price in self.price_data.items() 
                           if start_date <= date <= end_date}
            
            if not filtered_data:
                messagebox.showwarning("Warning", "No data in current view")
                return
            
            # Analyze
            context = self.analyze_financial_context(start_date, end_date, filtered_data)
            self._display_context_gui(context, f"Current View Analysis ({start_date} to {end_date})")
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {e}")
    
    def _analyze_crisis_period(self):
        """Analyze crisis period (2022)"""
        context = self.analyze_financial_context("2022-01-01", "2022-12-31", self.price_data)
        self._display_context_gui(context, "Crisis Period Analysis (2022)")
    
    def _analyze_recovery_period(self):
        """Analyze recovery period (2023)"""
        context = self.analyze_financial_context("2023-01-01", "2023-12-31", self.price_data)
        self._display_context_gui(context, "Recovery Period Analysis (2023)")
    
    def _analyze_recent_performance(self):
        """Analyze recent 6 months performance"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        context = self.analyze_financial_context(start_str, end_str, self.price_data)
        self._display_context_gui(context, f"Recent Performance Analysis ({start_str} to {end_str})")
    
    def _analyze_custom_range(self):
        """Analyze custom date range"""
        start_date = simpledialog.askstring("Custom Analysis", "Enter start date (YYYY-MM-DD):")
        if not start_date:
            return
            
        end_date = simpledialog.askstring("Custom Analysis", "Enter end date (YYYY-MM-DD):")
        if not end_date:
            return
        
        try:
            context = self.analyze_financial_context(start_date, end_date, self.price_data)
            self._display_context_gui(context, f"Custom Range Analysis ({start_date} to {end_date})")
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {e}")
    
    def _display_context_gui(self, context: Dict, title: str = "Financial Context Analysis"):
        """Display financial context analysis in a GUI window"""
        if "error" in context:
            messagebox.showerror("Analysis Error", context["error"])
            return
        
        # Create new window for analysis results
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("800x600")
        result_window.configure(bg='#f0f0f0')
        
        # Create scrollable text widget
        text_frame = ttk.Frame(result_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                               font=('Arial', 10), width=80, height=30)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Format and insert analysis
        formatted_text = self._format_context_for_gui(context)
        text_widget.insert(tk.END, formatted_text)
        text_widget.config(state=tk.DISABLED)
        
        # Add close button
        close_btn = ttk.Button(result_window, text="Close", 
                              command=result_window.destroy)
        close_btn.pack(pady=10)
    
    def _create_interactive_buttons(self, fig, ax, df: pd.DataFrame, price_data: Dict[str, float]):
        """Create interactive buttons for financial context analysis"""
        print("Setting up button callbacks...")
        # Store references for button callbacks
        self.current_ax = ax
        self.current_price_data = price_data
        
        # Create button area
        button_area = plt.axes([0.02, 0.02, 0.96, 0.08])
        button_area.set_xticks([])
        button_area.set_yticks([])
        button_area.set_facecolor('lightgray')
        
        # Create buttons with simpler positioning
        button_width = 0.12
        button_height = 0.04
        button_spacing = 0.01
        start_x = 0.05
        start_y = 0.04
        
        # Button 1: Analyze Current Zoom
        ax_zoom = plt.axes([start_x, start_y, button_width, button_height])
        btn_zoom = Button(ax_zoom, 'Analyze\nCurrent Zoom', color='lightblue', hovercolor='lightcyan')
        btn_zoom.on_clicked(self._on_analyze_zoom_clicked)
        
        # Button 2: Custom Date Range
        ax_custom = plt.axes([start_x + button_width + button_spacing, start_y, button_width, button_height])
        btn_custom = Button(ax_custom, 'Custom\nDate Range', color='lightgreen', hovercolor='lightcyan')
        btn_custom.on_clicked(self._on_custom_range_clicked)
        
        # Button 3: Crisis Period (2022)
        ax_crisis = plt.axes([start_x + 2*(button_width + button_spacing), start_y, button_width, button_height])
        btn_crisis = Button(ax_crisis, 'Crisis\nPeriod 2022', color='lightcoral', hovercolor='lightcyan')
        btn_crisis.on_clicked(self._on_crisis_period_clicked)
        
        # Button 4: Recovery Period (2023)
        ax_recovery = plt.axes([start_x + 3*(button_width + button_spacing), start_y, button_width, button_height])
        btn_recovery = Button(ax_recovery, 'Recovery\nPeriod 2023', color='lightgreen', hovercolor='lightcyan')
        btn_recovery.on_clicked(self._on_recovery_period_clicked)
        
        # Button 5: Recent Performance
        ax_recent = plt.axes([start_x + 4*(button_width + button_spacing), start_y, button_width, button_height])
        btn_recent = Button(ax_recent, 'Recent\n6 Months', color='lightyellow', hovercolor='lightcyan')
        btn_recent.on_clicked(self._on_recent_performance_clicked)
        
        # Button 6: Show Help
        ax_help = plt.axes([start_x + 5*(button_width + button_spacing), start_y, button_width, button_height])
        btn_help = Button(ax_help, 'Help\n& Info', color='lightgray', hovercolor='lightcyan')
        btn_help.on_clicked(self._on_help_clicked)
        
        # Add instructions text
        button_area.text(0.5, 0.5, 'Click buttons below to analyze financial context for different periods', 
                        ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Store button references to prevent garbage collection
        self.buttons = [btn_zoom, btn_custom, btn_crisis, btn_recovery, btn_recent, btn_help]
        print(f"Created {len(self.buttons)} buttons successfully!")
    
    def _on_analyze_zoom_clicked(self, event):
        """Callback for analyze current zoom button"""
        print("Analyze zoom button clicked!")
        self._analyze_current_zoom(self.current_ax, self.current_price_data)
    
    def _on_custom_range_clicked(self, event):
        """Callback for custom date range button"""
        print("Custom range button clicked!")
        self._analyze_custom_range_gui(self.current_price_data)
    
    def _on_crisis_period_clicked(self, event):
        """Callback for crisis period button"""
        print("Crisis period button clicked!")
        self._analyze_crisis_period_gui(self.current_price_data)
    
    def _on_recovery_period_clicked(self, event):
        """Callback for recovery period button"""
        print("Recovery period button clicked!")
        self._analyze_recovery_period_gui(self.current_price_data)
    
    def _on_recent_performance_clicked(self, event):
        """Callback for recent performance button"""
        print("Recent performance button clicked!")
        self._analyze_recent_performance_gui(self.current_price_data)
    
    def _on_help_clicked(self, event):
        """Callback for help button"""
        print("Help button clicked!")
        self._show_help_gui()
    
    def _analyze_current_zoom(self, ax, price_data: Dict[str, float]):
        """Analyze the currently zoomed area of the graph"""
        try:
            # Get current x-axis limits
            xlim = ax.get_xlim()
            
            # Convert matplotlib dates to datetime
            start_date = pd.to_datetime(xlim[0], unit='D', origin='1899-12-30').strftime('%Y-%m-%d')
            end_date = pd.to_datetime(xlim[1], unit='D', origin='1899-12-30').strftime('%Y-%m-%d')
            
            # Perform analysis
            context = self.analyze_financial_context(start_date, end_date, price_data)
            self._display_context_gui(context, f"Zoom Analysis ({start_date} to {end_date})")
            
        except Exception as e:
            self._show_error_gui(f"Error analyzing current zoom: {str(e)}")
    
    def _analyze_custom_range_gui(self, price_data: Dict[str, float]):
        """Show GUI dialog for custom date range analysis"""
        try:
            # Create a simple dialog for date input
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            start_date = simpledialog.askstring("Custom Date Range", 
                                              "Enter start date (YYYY-MM-DD):", 
                                              parent=root)
            if start_date:
                end_date = simpledialog.askstring("Custom Date Range", 
                                                "Enter end date (YYYY-MM-DD):", 
                                                parent=root)
                if end_date:
                    # Validate dates
                    datetime.strptime(start_date, "%Y-%m-%d")
                    datetime.strptime(end_date, "%Y-%m-%d")
                    
                    # Perform analysis
                    context = self.analyze_financial_context(start_date, end_date, price_data)
                    self._display_context_gui(context, f"Custom Analysis ({start_date} to {end_date})")
            
            root.destroy()
            
        except ValueError:
            self._show_error_gui("Invalid date format. Please use YYYY-MM-DD format.")
        except Exception as e:
            self._show_error_gui(f"Error in custom analysis: {str(e)}")
    
    def _analyze_crisis_period_gui(self, price_data: Dict[str, float]):
        """Analyze crisis period (2022) with GUI"""
        context = self.analyze_financial_context("2022-01-01", "2022-12-31", price_data)
        self._display_context_gui(context, "Crisis Period Analysis (2022)")
    
    def _analyze_recovery_period_gui(self, price_data: Dict[str, float]):
        """Analyze recovery period (2023) with GUI"""
        context = self.analyze_financial_context("2023-01-01", "2023-12-31", price_data)
        self._display_context_gui(context, "Recovery Period Analysis (2023)")
    
    def _analyze_recent_performance_gui(self, price_data: Dict[str, float]):
        """Analyze recent performance (last 6 months) with GUI"""
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=180)  # 6 months
        
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        context = self.analyze_financial_context(start_date_str, end_date_str, price_data)
        self._display_context_gui(context, "Recent Performance Analysis (Last 6 Months)")
    
    def _display_context_gui(self, context: Dict[str, any], title: str):
        """Display financial context analysis in a GUI window"""
        if "error" in context:
            self._show_error_gui(context["error"])
            return
        
        # Create a new window for displaying the analysis
        root = tk.Tk()
        root.title(f"Financial Context Analysis - {title}")
        root.geometry("800x600")
        
        # Create a text widget with scrollbar
        text_frame = tk.Frame(root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Format and insert the analysis
        analysis_text = self._format_context_for_gui(context)
        text_widget.insert(tk.END, analysis_text)
        text_widget.config(state=tk.DISABLED)  # Make it read-only
        
        # Add close button
        close_btn = tk.Button(root, text="Close", command=root.destroy, 
                             font=("Arial", 12), bg="lightblue")
        close_btn.pack(pady=10)
        
        root.mainloop()
    
    def _format_context_for_gui(self, context: Dict[str, any]) -> str:
        """Format the financial context for GUI display"""
        text = f"""
📊 FINANCIAL CONTEXT ANALYSIS
{'='*60}

📅 Period: {context['date_range']}
📈 Total Return: {context['total_return']}%
📊 Volatility: {context['volatility']}%
💰 Price Range: {context['price_range']}
📋 Data Points: {context['data_points']}

📈 TREND ANALYSIS:
  Direction: {context['trend_analysis']['direction']}
  Strength: {context['trend_analysis']['strength']}%
  Description: {context['trend_analysis']['description']}

"""
        
        if context['contextual_events']:
            text += "🎯 KEY EVENTS DURING THIS PERIOD:\n"
            for event in context['contextual_events']:
                impact_emoji = "🔴" if event.get("impact") == "High" else "🟡" if event.get("impact") == "Medium" else "🟢"
                text += f"  {impact_emoji} {event['date']}: {event['event']}\n"
            text += "\n"
        
        text += "💡 AI INSIGHTS:\n"
        for insight in context['insights']:
            text += f"  {insight}\n"
        
        text += f"\n{'='*60}\n"
        text += "💡 This analysis helps you understand what happened in Sri Lanka's\n"
        text += "   financial sector during the selected period and how it may have\n"
        text += "   influenced the fund's performance.\n"
        
        return text
    
    def _show_error_gui(self, error_message: str):
        """Show error message in a GUI dialog"""
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", error_message)
        root.destroy()
    
    def _show_help_gui(self):
        """Show help information in a GUI window"""
        root = tk.Tk()
        root.title("Financial Context Analysis - Help")
        root.geometry("600x500")
        
        help_text = """
🔍 FINANCIAL CONTEXT ANALYSIS - HELP

This feature provides AI-powered insights about Sri Lankan financial 
sector events during selected date ranges to help you understand 
what influenced fund performance.

📊 AVAILABLE ANALYSES:

🔍 Analyze Current Zoom
   - Analyzes the currently visible date range on the graph
   - Use zoom/pan to select your area of interest, then click this button

📅 Custom Date Range  
   - Enter any specific date range for analysis
   - Useful for analyzing specific events or periods

🚨 Crisis Period 2022
   - Analyzes the Sri Lankan economic crisis period
   - Shows impact of debt default, IMF negotiations, etc.

📈 Recovery Period 2023
   - Analyzes the post-crisis recovery period
   - Shows impact of IMF bailout and recovery measures

📊 Recent 6 Months
   - Analyzes the most recent performance
   - Shows current market conditions and trends

💡 WHAT YOU GET:

• Performance Metrics: Total return, volatility, price ranges
• Trend Analysis: Uptrend/downtrend detection with strength
• Event Correlation: Major Sri Lankan financial events
• AI Insights: Explanations for performance changes
• Context Understanding: Why prices moved up or down

🎯 HOW TO USE:

1. Zoom into the area you want to analyze
2. Click "Analyze Current Zoom" for that specific period
3. Or use predefined periods for major events
4. Read the analysis to understand market context

This helps you make informed investment decisions based on 
historical context and market events.
        """
        
        text_widget = tk.Text(root, wrap=tk.WORD, font=("Consolas", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        close_btn = tk.Button(root, text="Close", command=root.destroy, 
                             font=("Arial", 12), bg="lightblue")
        close_btn.pack(pady=10)
        
        root.mainloop()
    
    
    def _apply_date_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply date filtering to reduce data points"""
        print(f"\nCurrent data range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
        
        # Get filter start date
        while True:
            start_input = input("Enter filter start date (YYYY-MM-DD) or press Enter to skip: ").strip()
            if not start_input:
                filter_start = df['Date'].min()
                break
            try:
                filter_start = pd.to_datetime(start_input)
                if filter_start >= df['Date'].min():
                    break
                else:
                    print("Start date must be within the data range")
            except:
                print("Invalid date format. Please use YYYY-MM-DD")
        
        # Get filter end date
        while True:
            end_input = input("Enter filter end date (YYYY-MM-DD) or press Enter to skip: ").strip()
            if not end_input:
                filter_end = df['Date'].max()
                break
            try:
                filter_end = pd.to_datetime(end_input)
                if filter_end <= df['Date'].max() and filter_end >= filter_start:
                    break
                else:
                    print("End date must be within the data range and after start date")
            except:
                print("Invalid date format. Please use YYYY-MM-DD")
        
        # Apply filter
        filtered_df = df[(df['Date'] >= filter_start) & (df['Date'] <= filter_end)]
        print(f"Filtered data: {len(filtered_df)} points from {filtered_df['Date'].min().strftime('%Y-%m-%d')} to {filtered_df['Date'].max().strftime('%Y-%m-%d')}")
        
        return filtered_df
    
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

    def init_all_funds_data(self, sample_date: str = None) -> Dict[str, Dict[str, float]]:
        """Initialize data collection for all available funds using smart caching and single API call per date"""
        # Use current date - 10 if no sample date provided
        if sample_date is None:
            sample_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        
        print(f"Initializing data collection for all funds using sample date: {sample_date}")
        
        # First, discover all available funds
        fund_data = self.fetch_fund_data(sample_date)
        if not fund_data or 'UTMS_FUND' not in fund_data:
            print("Failed to fetch fund data for initialization")
            return {}
        
        # Get all fund names
        available_funds = []
        for fund in fund_data['UTMS_FUND']:
            fund_name = fund.get('FUND_NAME')
            if fund_name:
                available_funds.append(fund_name)
        
        print(f"Found {len(available_funds)} available funds:")
        for i, fund in enumerate(available_funds, 1):
            print(f"  {i:2d}. {fund}")
        
        # Initialize data structure for all funds and load existing data
        all_funds_data = {}
        existing_data_summary = {}
        
        for fund_name in available_funds:
            # Create a temporary extractor for this fund to load existing data
            temp_extractor = CALFundExtractor(fund_name, self.start_date, self.end_date, self.api_delay)
            existing_data = temp_extractor.load_existing_data()
            all_funds_data[fund_name] = existing_data.copy()
            existing_data_summary[fund_name] = len(existing_data)
        
        # Generate date range
        dates = self.generate_date_range()
        
        # Calculate missing dates for each fund
        missing_dates_by_fund = {}
        total_missing_dates = set()
        
        for fund_name in available_funds:
            missing_dates = [date for date in dates if date not in all_funds_data[fund_name]]
            missing_dates_by_fund[fund_name] = missing_dates
            total_missing_dates.update(missing_dates)
        
        # Show data coverage summary
        print(f"\nData Coverage Summary:")
        print(f"  Total dates in range: {len(dates)}")
        print(f"  Unique dates needing API calls: {len(total_missing_dates)}")
        
        total_existing = sum(existing_data_summary.values())
        total_possible = len(dates) * len(available_funds)
        print(f"  Existing data points: {total_existing}/{total_possible}")
        
        if total_missing_dates:
            print(f"  Missing data range: {min(total_missing_dates)} to {max(total_missing_dates)}")
            print(f"  🔄 Fetching from API for {len(total_missing_dates)} dates...")
            
            successful_fetches = 0
            failed_fetches = 0
            
            for i, date in enumerate(sorted(total_missing_dates), 1):
                print(f"  Processing missing date {i}/{len(total_missing_dates)}: {date}")
                
                fund_data = self.fetch_fund_data(date)
                if fund_data and 'UTMS_FUND' in fund_data:
                    # Extract data for all funds from this date
                    date_success_count = 0
                    for fund in fund_data['UTMS_FUND']:
                        fund_name = fund.get('FUND_NAME')
                        if fund_name in all_funds_data:
                            try:
                                price = float(fund.get('OLD_PRICE', 0))
                                if price > 0:  # Only store valid prices
                                    all_funds_data[fund_name][date] = price
                                    date_success_count += 1
                            except (ValueError, TypeError):
                                continue
                    
                    if date_success_count > 0:
                        successful_fetches += 1
                        print(f"    ✓ Collected data for {date_success_count}/{len(available_funds)} funds")
                    else:
                        failed_fetches += 1
                        print(f"    ⚠ No valid data for any fund on this date")
                else:
                    failed_fetches += 1
                    print(f"    ⚠ Failed to fetch data for this date")
                
                # Add configurable delay to be respectful to the API
                time.sleep(self.api_delay)
            
            print(f"\nFetch Summary:")
            print(f"  ✓ Successfully fetched: {successful_fetches} dates")
            print(f"  ⚠ Failed to fetch: {failed_fetches} dates")
        else:
            print(f"  ✅ All {len(dates)} dates already have data for all funds - no API calls needed!")
        
        # Save data for each fund (only if there's new data)
        saved_files = []
        updated_files = []
        
        for fund_name, price_data in all_funds_data.items():
            if price_data:  # Only save if we have data
                # Create filename for this fund
                csv_filename = f'cal_fund_data_{fund_name.replace(" ", "_").replace("/", "_")}.csv'
                
                # Check if file already exists
                file_exists = os.path.exists(csv_filename)
                
                # Save to CSV
                df = pd.DataFrame(list(price_data.items()), columns=['Date', 'OLD_PRICE'])
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')
                df.to_csv(csv_filename, index=False)
                
                if file_exists:
                    updated_files.append(csv_filename)
                    print(f"  🔄 Updated {len(price_data)} data points for '{fund_name}' in '{csv_filename}'")
                else:
                    saved_files.append(csv_filename)
                    print(f"  ✓ Saved {len(price_data)} data points for '{fund_name}' to '{csv_filename}'")
        
        print(f"\nFile Summary:")
        print(f"  📁 New files created: {len(saved_files)}")
        print(f"  🔄 Existing files updated: {len(updated_files)}")
        
        return all_funds_data
    
    def analyze_financial_context(self, start_date: str, end_date: str, price_data: Dict[str, float]) -> Dict[str, any]:
        """Analyze financial context for a given date range"""
        print(f"\n🔍 Analyzing financial context for {start_date} to {end_date}")
        print("=" * 60)
        
        # Convert dates for analysis
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Filter price data for the selected range
        filtered_data = {}
        for date_str, price in price_data.items():
            date_dt = datetime.strptime(date_str, "%Y-%m-%d")
            if start_dt <= date_dt <= end_dt:
                filtered_data[date_str] = price
        
        if not filtered_data:
            return {"error": "No data available for the selected date range"}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(list(filtered_data.items()), columns=['Date', 'Price'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        # Calculate performance metrics
        start_price = df['Price'].iloc[0]
        end_price = df['Price'].iloc[-1]
        total_return = ((end_price - start_price) / start_price) * 100
        
        # Calculate volatility
        returns = df['Price'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) * 100  # Annualized volatility
        
        # Find significant price movements
        price_changes = df['Price'].diff()
        significant_moves = price_changes[abs(price_changes) > price_changes.std() * 2]
        
        # Analyze trends
        trend_analysis = self._analyze_trend(df)
        
        # Get contextual events
        contextual_events = self._get_contextual_events(start_date, end_date)
        
        # Generate insights
        insights = self._generate_insights(df, total_return, volatility, significant_moves, contextual_events)
        
        return {
            "date_range": f"{start_date} to {end_date}",
            "total_return": round(total_return, 2),
            "volatility": round(volatility, 2),
            "price_range": f"{df['Price'].min():.4f} - {df['Price'].max():.4f}",
            "data_points": len(df),
            "trend_analysis": trend_analysis,
            "significant_moves": len(significant_moves),
            "contextual_events": contextual_events,
            "insights": insights
        }
    
    def _analyze_trend(self, df: pd.DataFrame) -> Dict[str, any]:
        """Analyze price trend in the selected period"""
        prices = df['Price'].values
        dates = np.arange(len(prices))
        
        # Linear regression to determine trend
        coeffs = np.polyfit(dates, prices, 1)
        slope = coeffs[0]
        
        # Calculate trend strength
        trend_strength = abs(slope) / prices.mean() * 100
        
        if slope > 0:
            trend_direction = "Uptrend"
            trend_description = f"Strong upward trend with {trend_strength:.2f}% daily growth"
        elif slope < 0:
            trend_direction = "Downtrend"
            trend_description = f"Declining trend with {abs(trend_strength):.2f}% daily decline"
        else:
            trend_direction = "Sideways"
            trend_description = "Relatively stable with minimal trend"
        
        return {
            "direction": trend_direction,
            "strength": round(trend_strength, 2),
            "description": trend_description
        }
    
    def _get_contextual_events(self, start_date: str, end_date: str) -> List[Dict[str, str]]:
        """Get contextual financial events for Sri Lanka during the date range"""
        # This is a simplified version - in a real implementation, you'd integrate with news APIs
        events = []
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Known significant events in Sri Lankan financial history
        significant_events = [
            {"date": "2022-03-01", "event": "Sri Lanka economic crisis begins", "impact": "High"},
            {"date": "2022-04-01", "event": "Sri Lanka defaults on foreign debt", "impact": "High"},
            {"date": "2022-07-01", "event": "IMF bailout negotiations begin", "impact": "Medium"},
            {"date": "2023-03-01", "event": "IMF approves $3 billion bailout package", "impact": "High"},
            {"date": "2023-09-01", "event": "Central Bank policy rate adjustments", "impact": "Medium"},
            {"date": "2024-01-01", "event": "Economic recovery measures implemented", "impact": "Medium"},
            {"date": "2024-06-01", "event": "Tourism sector recovery", "impact": "Low"},
        ]
        
        for event in significant_events:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            if start_dt <= event_date <= end_dt:
                events.append(event)
        
        # Add general market context based on the period
        if start_dt.year == 2022:
            events.append({
                "date": "2022",
                "event": "Global economic uncertainty and inflation pressures",
                "impact": "High"
            })
        elif start_dt.year == 2023:
            events.append({
                "date": "2023",
                "event": "Post-crisis recovery and IMF program implementation",
                "impact": "High"
            })
        elif start_dt.year == 2024:
            events.append({
                "date": "2024",
                "event": "Economic stabilization and growth initiatives",
                "impact": "Medium"
            })
        
        return events
    
    def _generate_insights(self, df: pd.DataFrame, total_return: float, volatility: float, 
                          significant_moves: pd.Series, events: List[Dict[str, str]]) -> List[str]:
        """Generate AI-powered insights about the fund performance"""
        insights = []
        
        # Performance insights
        if total_return > 10:
            insights.append("📈 Strong positive performance during this period")
        elif total_return > 5:
            insights.append("📊 Moderate positive performance")
        elif total_return > 0:
            insights.append("📉 Slight positive performance")
        elif total_return > -5:
            insights.append("📉 Minor decline in performance")
        elif total_return > -10:
            insights.append("📉 Moderate decline in performance")
        else:
            insights.append("📉 Significant decline in performance")
        
        # Volatility insights
        if volatility > 30:
            insights.append("⚡ High volatility period - significant price swings")
        elif volatility > 20:
            insights.append("📊 Moderate volatility - some price fluctuations")
        else:
            insights.append("📈 Low volatility - relatively stable period")
        
        # Event correlation insights
        if events:
            high_impact_events = [e for e in events if e.get("impact") == "High"]
            if high_impact_events:
                insights.append(f"🎯 {len(high_impact_events)} high-impact economic events occurred during this period")
                insights.append("💡 Performance likely influenced by major economic developments")
        
        # Trend insights
        if len(significant_moves) > 0:
            insights.append(f"📊 {len(significant_moves)} significant price movements detected")
            insights.append("🔍 These movements may indicate market reactions to news or events")
        
        # Data quality insights
        if len(df) < 5:
            insights.append("⚠️ Limited data points - analysis may be less reliable")
        elif len(df) > 20:
            insights.append("✅ Sufficient data points for reliable analysis")
        
        return insights
    

def get_user_fund_selection(available_funds: List[str], earliest_dates: Dict[str, str]) -> str:
    """Get fund selection from user with earliest dates displayed"""
    print("\nAvailable Funds:")
    print("-" * 80)
    for i, fund in enumerate(available_funds, 1):
        earliest_date = earliest_dates.get(fund, "2013-01-01")
        print(f"{i:2d}. {fund}")
        print(f"    📅 Data available from: {earliest_date}")
    
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

def get_user_api_delay_input(prompt: str, default: float) -> float:
    """Get API delay input from user with validation"""
    while True:
        user_input = input(f"{prompt} (default: {default} seconds): ").strip()
        if not user_input:
            return default
        
        try:
            delay = float(user_input)
            if delay < 0:
                print("Delay must be 0 or greater")
                continue
            if delay == 0:
                print("Warning: No delay may overload the server and cause rate limiting")
                confirm = input("Continue with no delay? (y/n): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    continue
            elif delay > 10:
                print("Warning: Delay greater than 10 seconds may significantly slow down data collection")
                confirm = input("Continue anyway? (y/n): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    continue
            return delay
        except ValueError:
            print("Invalid delay format. Please enter a number (e.g., 0, 0.5, 1.0, 2)")

def main():
    """Main function to run the fund data extraction and visualization"""
    print("CAL Fund Data Extractor")
    print("=" * 50)
    
    # Check for init command
    if len(sys.argv) > 1 and sys.argv[1].lower() == "init":
        print("Running INIT command - collecting data for all available funds")
        print("=" * 50)
        
        # Get date range from user (with earliest available date as default)
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Get earliest date across all funds for init mode
        temp_extractor = CALFundExtractor()
        earliest_dates = temp_extractor.get_all_funds_earliest_dates()
        
        # Find the earliest date across all funds
        if earliest_dates:
            earliest_overall = min(earliest_dates.values())
            print(f"\nEarliest data available across all funds: {earliest_overall}")
        else:
            earliest_overall = "2013-01-01"
        
        start_date = get_user_date_input("Enter start date (YYYY-MM-DD)", earliest_overall)
        end_date = get_user_date_input("Enter end date (YYYY-MM-DD)", yesterday)
        
        # Get API delay from user
        api_delay = get_user_api_delay_input("Enter API delay between requests", 0.5)
        
        # Create extractor for init command
        extractor = CALFundExtractor(None, start_date, end_date, api_delay)
        
        print("\n" + "=" * 50)
        print(f"INIT Mode: Collecting data for ALL available funds")
        print(f"Date Range: {extractor.start_date} - {extractor.end_date} (1st & 15th of each month)")
        print(f"API Delay: {extractor.api_delay} seconds between requests")
        print("=" * 50)
        
        # Run init command
        all_funds_data = extractor.init_all_funds_data()
        
        if all_funds_data:
            total_funds = len([fund for fund, data in all_funds_data.items() if data])
            print(f"\n✅ INIT completed successfully!")
            print(f"📊 Collected data for {total_funds} funds")
            print(f"📁 Created CSV files for each fund")
            print(f"\nYou can now run the normal mode to analyze specific funds:")
            print(f"  python cal_fund_extractor.py")
        else:
            print("❌ INIT failed - no data was collected")
        
        return
    
    # Normal mode - single fund analysis
    print("Running in NORMAL mode - analyzing a specific fund")
    print("=" * 50)
    
    # Create a temporary extractor to discover available funds and their earliest dates
    temp_extractor = CALFundExtractor()
    available_funds = temp_extractor.discover_available_funds()
    
    if not available_funds:
        print("Failed to discover available funds. Using default fund.")
        selected_fund = "Capital Alliance Quantitative Equity Fund"
        earliest_dates = {selected_fund: "2013-01-01"}
    else:
        # Get earliest dates for all funds
        earliest_dates = temp_extractor.get_all_funds_earliest_dates()
        selected_fund = get_user_fund_selection(available_funds, earliest_dates)
    
    # Get date range from user (with fund-specific defaults)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    fund_earliest_date = earliest_dates.get(selected_fund, "2013-01-01")
    start_date = get_user_date_input("Enter start date (YYYY-MM-DD)", fund_earliest_date)
    end_date = get_user_date_input("Enter end date (YYYY-MM-DD)", yesterday)
    
    # Get API delay from user
    api_delay = get_user_api_delay_input("Enter API delay between requests", 0.5)
    
    # Create the main extractor with user selections
    extractor = CALFundExtractor(selected_fund, start_date, end_date, api_delay)
    
    print("\n" + "=" * 50)
    print(f"Target Fund: {extractor.target_fund_name}")
    print(f"Date Range: {extractor.start_date} - {extractor.end_date} (1st & 15th of each month)")
    print(f"API Delay: {extractor.api_delay} seconds between requests")
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
