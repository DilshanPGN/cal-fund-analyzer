"""
CAL API Service - Handles all interactions with the Capital Alliance API.
Implements the Service Pattern for clean separation of concerns.
"""

import requests
from typing import Dict, Optional, Any
from datetime import datetime
import logging

from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CALAPIService:
    """
    Service class for interacting with the Capital Alliance API.
    
    This class implements the Service Pattern, encapsulating all business logic
    related to the external CAL API.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the CAL API service.
        
        Args:
            config: Configuration object containing API settings
        """
        self.base_url = config.CAL_API_BASE_URL
        self.timeout = config.API_TIMEOUT
        self.config = config
        
    def fetch_fund_rates(self, date: str) -> Optional[Dict[str, Any]]:
        """
        Fetch fund rates for a specific date.
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Dictionary containing fund data, or None if request fails
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        try:
            params = self.config.get_api_params(date)
            
            logger.info(f"Fetching fund rates for date: {date}")
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Successfully fetched fund rates for {date}")
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for date: {date}")
            raise
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for date {date}: {str(e)}")
            raise
            
        except ValueError as e:
            logger.error(f"Invalid JSON response for date {date}: {str(e)}")
            raise
    
    def get_available_funds(self, sample_date: Optional[str] = None) -> list:
        """
        Get list of available funds from the API.
        
        Args:
            sample_date: Date to use for sampling funds. If None, uses today's date.
            
        Returns:
            List of fund names
        """
        if sample_date is None:
            sample_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            data = self.fetch_fund_rates(sample_date)
            
            if not data or 'UTMS_FUND' not in data:
                logger.warning("No UTMS_FUND data in response")
                return []
            
            funds = [
                fund.get('FUND_NAME')
                for fund in data['UTMS_FUND']
                if fund.get('FUND_NAME')
            ]
            
            logger.info(f"Found {len(funds)} available funds")
            return funds
            
        except Exception as e:
            logger.error(f"Failed to fetch available funds: {str(e)}")
            return []
    
    def validate_date(self, date_str: str) -> bool:
        """
        Validate date string format.
        
        Args:
            date_str: Date string to validate
            
        Returns:
            True if date is valid, False otherwise
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the API.
        
        Returns:
            Dictionary with health status
        """
        try:
            # Try to fetch data for a recent date
            test_date = datetime.now().strftime('%Y-%m-%d')
            data = self.fetch_fund_rates(test_date)
            
            return {
                'status': 'healthy',
                'api_accessible': True,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'api_accessible': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

