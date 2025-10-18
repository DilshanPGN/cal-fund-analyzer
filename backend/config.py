"""
Configuration settings for the CAL Fund Analyzer backend.
Contains all application configuration in one place.
"""

import os
from typing import Dict, Any


class Config:
    """Base configuration class."""
    
    # Flask settings
    DEBUG = True
    TESTING = False
    
    # Server settings
    HOST = '0.0.0.0'
    PORT = 5000
    
    # API settings
    CAL_API_BASE_URL = 'https://cal.lk/wp-admin/admin-ajax.php'
    API_TIMEOUT = 10  # seconds
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    
    # Rate limiting
    REQUEST_DELAY = 0.5  # seconds between requests
    
    @staticmethod
    def get_api_params(date: str) -> Dict[str, str]:
        """
        Get standard API parameters for CAL API requests.
        
        Args:
            date: Date string in YYYY-MM-DD format
            
        Returns:
            Dictionary of API parameters
        """
        return {
            'action': 'getUTFundRates',
            'valuedate': date
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config: Dict[str, Any] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env: str = 'default') -> Config:
    """
    Get configuration based on environment.
    
    Args:
        env: Environment name (development, production, testing, default)
        
    Returns:
        Configuration class instance
    """
    return config.get(env, config['default'])

